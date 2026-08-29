#!/usr/bin/env python3
"""Collect a read-only snapshot of a repository's open issues for roadmap analysis.

Writes two files into an output directory and prints a compact index to stdout:

- snapshot.json  machine-readable data (open issues, open pull requests,
                 sub-issue links, cross references, resolved referenced items)
- issues.md      every open issue's body and comments in ID order, for reading

Requires an authenticated GitHub CLI (`gh`).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SHORT_REFERENCE = re.compile(r"(?<![\w/])#(\d+)\b")
QUALIFIED_REFERENCE = re.compile(
    r"(?:https?://github\.com/)?([\w.-]+)/([\w.-]+)(?:#|/(?:issues|pull)/)(\d+)\b"
)
PAGE_SIZE = 50
REFERENCE_BATCH = 40

ISSUE_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    issues(states: OPEN, first: %d, after: $cursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url createdAt updatedAt body
        author { login }
        labels(first: 20) { nodes { name } }
        milestone { title }
        assignees(first: 10) { nodes { login } }
        parent { number }
        subIssues(first: 100) { totalCount nodes { number state } }
        comments(first: 50) {
          totalCount
          nodes { author { login } createdAt body }
        }
        closedByPullRequestsReferences(first: 10, includeClosedPrs: true) {
          nodes { number state merged }
        }
        timelineItems(itemTypes: [CROSS_REFERENCED_EVENT], first: 50) {
          nodes {
            ... on CrossReferencedEvent {
              source {
                ... on Issue { number state repository { nameWithOwner } }
                ... on PullRequest { number state merged repository { nameWithOwner } }
              }
            }
          }
        }
      }
    }
  }
}
""" % PAGE_SIZE

PULL_REQUEST_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: OPEN, first: %d, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url isDraft updatedAt body
        author { login }
        closingIssuesReferences(first: 20) { nodes { number } }
      }
    }
  }
}
""" % PAGE_SIZE

REFERENCE_FRAGMENT = """
    r%d: issueOrPullRequest(number: %d) {
      __typename
      ... on Issue {
        number title state closedAt
        closedByPullRequestsReferences(first: 5, includeClosedPrs: true) { nodes { number merged } }
      }
      ... on PullRequest { number title state merged mergedAt }
    }"""


class CollectionError(RuntimeError):
    """A concise error safe to show directly to the user."""


def graphql(query: str, **variables: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Run a GraphQL query. Returns (data, errors); partial data is kept."""
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is not None:
            command += ["-F", f"{key}={value}"]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        payload = {}
    data = payload.get("data") or {}
    errors = payload.get("errors") or []
    if result.returncode != 0 and not data:
        detail = result.stderr.strip() or "unknown gh error"
        raise CollectionError(f"gh api graphql failed: {detail}")
    return data, errors


def resolve_repository(argument: str | None) -> str:
    if argument:
        match = re.fullmatch(
            r"(?:https://github\.com/)?([^/\s]+)/([^/\s]+?)(?:\.git)?/?", argument
        )
        if not match:
            raise CollectionError(
                "repository must be OWNER/REPO or https://github.com/OWNER/REPO"
            )
        return f"{match.group(1)}/{match.group(2)}"
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise CollectionError(
            "repository was not specified and could not be inferred from the current "
            f"checkout: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def paginate(query: str, owner: str, name: str, connection: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    cursor = None
    while True:
        data, errors = graphql(query, owner=owner, name=name, cursor=cursor)
        repository = data.get("repository")
        if repository is None:
            messages = "; ".join(error.get("message", "") for error in errors) or "no data"
            raise CollectionError(f"could not read {owner}/{name}: {messages}")
        page = repository[connection]
        nodes.extend(node for node in page["nodes"] if node)
        print(f"fetched {len(nodes)} {connection}...", file=sys.stderr, end="\r")
        if not page["pageInfo"]["hasNextPage"]:
            return nodes
        cursor = page["pageInfo"]["endCursor"]


def text_references(text: str, repository: str) -> tuple[set[int], set[str]]:
    """Return (same-repo numbers, other-repo 'owner/repo#N' strings) mentioned in text."""
    same: set[int] = set()
    other: set[str] = set()
    for owner, name, number in QUALIFIED_REFERENCE.findall(text):
        full = f"{owner}/{name}"
        if full.lower() == repository.lower():
            same.add(int(number))
        else:
            other.add(f"{full}#{number}")
    stripped = QUALIFIED_REFERENCE.sub(" ", text)
    same.update(int(number) for number in SHORT_REFERENCE.findall(stripped))
    return same, other


def nodes_of(connection: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Nodes of a GraphQL connection, skipping entries the token cannot see."""
    return [node for node in (connection or {}).get("nodes") or [] if node]


def normalize_issue(node: dict[str, Any], repository: str) -> dict[str, Any]:
    texts = [node.get("body") or ""] + [c.get("body") or "" for c in nodes_of(node["comments"])]
    mentioned: set[int] = set()
    external: set[str] = set()
    for text in texts:
        same, other = text_references(text, repository)
        mentioned.update(same)
        external.update(other)

    referenced_by: list[dict[str, Any]] = []
    for item in nodes_of(node["timelineItems"]):
        source = item.get("source") or {}
        if not source.get("number"):
            continue
        entry = {
            "number": source["number"],
            "kind": "pull_request" if "merged" in source else "issue",
            "state": source["state"],
        }
        if "merged" in source:
            entry["merged"] = source["merged"]
        if source["repository"]["nameWithOwner"].lower() != repository.lower():
            entry["repository"] = source["repository"]["nameWithOwner"]
        referenced_by.append(entry)

    return {
        "number": node["number"],
        "title": node["title"],
        "url": node["url"],
        "author": (node.get("author") or {}).get("login"),
        "createdAt": node["createdAt"],
        "updatedAt": node["updatedAt"],
        "labels": [label["name"] for label in nodes_of(node["labels"])],
        "milestone": (node.get("milestone") or {}).get("title"),
        "assignees": [user["login"] for user in nodes_of(node["assignees"])],
        "parent": (node.get("parent") or {}).get("number"),
        "subIssues": [
            {"number": sub["number"], "state": sub["state"]}
            for sub in nodes_of(node["subIssues"])
        ],
        "subIssueCount": node["subIssues"]["totalCount"],
        "mentions": sorted(mentioned - {node["number"]}),
        "externalMentions": sorted(external),
        "referencedBy": referenced_by,
        "closingPullRequests": [
            {"number": pr["number"], "state": pr["state"], "merged": pr["merged"]}
            for pr in nodes_of(node["closedByPullRequestsReferences"])
        ],
        "body": node.get("body") or "",
        "commentCount": node["comments"]["totalCount"],
        "comments": [
            {
                "author": (comment.get("author") or {}).get("login"),
                "createdAt": comment["createdAt"],
                "body": comment.get("body") or "",
            }
            for comment in nodes_of(node["comments"])
        ],
    }


def normalize_pull_request(node: dict[str, Any], repository: str) -> dict[str, Any]:
    mentioned, _ = text_references(node.get("body") or "", repository)
    closes = [ref["number"] for ref in nodes_of(node["closingIssuesReferences"])]
    return {
        "number": node["number"],
        "title": node["title"],
        "url": node["url"],
        "author": (node.get("author") or {}).get("login"),
        "isDraft": node["isDraft"],
        "updatedAt": node["updatedAt"],
        "closes": closes,
        "mentions": sorted(mentioned - set(closes)),
    }


def resolve_references(
    owner: str, name: str, numbers: list[int]
) -> tuple[dict[int, dict[str, Any]], list[int]]:
    """Look up referenced items in batches; failures degrade to 'unresolved'."""
    resolved: dict[int, dict[str, Any]] = {}
    unresolved: list[int] = []
    for start in range(0, len(numbers), REFERENCE_BATCH):
        batch = numbers[start : start + REFERENCE_BATCH]
        body = "".join(REFERENCE_FRAGMENT % (number, number) for number in batch)
        query = "query($owner: String!, $name: String!) { repository(owner: $owner, name: $name) {%s\n} }" % body
        try:
            data, _ = graphql(query, owner=owner, name=name)
        except CollectionError as error:
            print(f"warning: {error}", file=sys.stderr)
            unresolved.extend(batch)
            continue
        repository = data.get("repository") or {}
        for number in batch:
            item = repository.get(f"r{number}")
            if not item:
                unresolved.append(number)
                continue
            entry = {
                "number": item["number"],
                "kind": "pull_request" if item["__typename"] == "PullRequest" else "issue",
                "title": item["title"],
                "state": item["state"],
            }
            if entry["kind"] == "pull_request":
                entry["merged"] = item["merged"]
                entry["mergedAt"] = item.get("mergedAt")
            else:
                entry["closedAt"] = item.get("closedAt")
                entry["closedBy"] = [
                    pr["number"] for pr in nodes_of(item.get("closedByPullRequestsReferences")) if pr["merged"]
                ]
            resolved[number] = entry
    return resolved, unresolved


def describe(number: int, known: dict[int, dict[str, Any]], open_issues: dict[int, dict[str, Any]]) -> str:
    if number in open_issues:
        return f"#{number}(open)"
    item = known.get(number)
    if item is None:
        return f"#{number}(?)"
    if item["kind"] == "pull_request":
        return f"#{number}(PR {'merged' if item['merged'] else item['state'].lower()})"
    if item.get("closedBy"):
        return f"#{number}(closed by merged PR " + " ".join(f"#{n}" for n in item["closedBy"]) + ")"
    return f"#{number}({item['state'].lower()})"


def write_issues_markdown(path: Path, snapshot: dict[str, Any]) -> None:
    lines = [f"# Open issues of {snapshot['repository']} at {snapshot['collectedAt']}", ""]
    for issue in snapshot["openIssues"]:
        lines.append(f"## #{issue['number']} {issue['title']}")
        meta = [f"updated {issue['updatedAt']}"]
        if issue["labels"]:
            meta.append("labels: " + ", ".join(issue["labels"]))
        if issue["milestone"]:
            meta.append(f"milestone: {issue['milestone']}")
        if issue["assignees"]:
            meta.append("assignees: " + ", ".join(issue["assignees"]))
        if issue["parent"]:
            meta.append(f"parent: #{issue['parent']}")
        if issue["subIssues"]:
            meta.append("sub-issues: " + ", ".join(f"#{s['number']}" for s in issue["subIssues"]))
        lines.append("_" + " | ".join(meta) + "_")
        lines.append("")
        lines.append(issue["body"].strip() or "(no body)")
        lines.append("")
        if not issue["comments"]:
            lines.append("(no comments)")
            lines.append("")
        for comment in issue["comments"]:
            lines.append(f"### comment by {comment['author']} at {comment['createdAt']}")
            lines.append("")
            lines.append(comment["body"].strip())
            lines.append("")
        if issue["commentCount"] > len(issue["comments"]):
            lines.append(
                f"(only {len(issue['comments'])} of {issue['commentCount']} comments shown; "
                f"run `gh issue view {issue['number']} --comments` for the rest)"
            )
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def print_index(snapshot: dict[str, Any], out_dir: Path) -> None:
    open_issues = {issue["number"]: issue for issue in snapshot["openIssues"]}
    known = {item["number"]: item for item in snapshot["references"]}
    print(f"{snapshot['repository']} at {snapshot['collectedAt']}: "
          f"{len(open_issues)} open issues, {len(snapshot['openPullRequests'])} open pull requests")
    print(f"snapshot: {out_dir / 'snapshot.json'}")
    print(f"bodies:   {out_dir / 'issues.md'}")
    print()
    # A number that references most open issues (a planning or tracking issue)
    # would repeat on every line; report it once instead.
    counts: dict[int, int] = {}
    for issue in snapshot["openIssues"]:
        for ref in issue["referencedBy"]:
            if "repository" not in ref:
                counts[ref["number"]] = counts.get(ref["number"], 0) + 1
    ubiquitous = {n for n, c in counts.items() if len(open_issues) >= 5 and c * 2 > len(open_issues)}
    if ubiquitous:
        print("referenced by most open issues (omitted below): "
              + " ".join(describe(n, known, open_issues) for n in sorted(ubiquitous)))
        print()
    print("## open issues (number | title | structure)")
    for issue in snapshot["openIssues"]:
        parts = []
        if issue["parent"]:
            parts.append(f"parent #{issue['parent']}")
        if issue["subIssues"]:
            parts.append("sub-issues " + " ".join(describe(s["number"], known, open_issues) for s in issue["subIssues"]))
        if issue["mentions"]:
            parts.append("mentions " + " ".join(describe(n, known, open_issues) for n in issue["mentions"]))
        if issue["externalMentions"]:
            parts.append("external " + " ".join(issue["externalMentions"]))
        referenced_by = [r for r in issue["referencedBy"] if r["number"] not in ubiquitous or "repository" in r]
        if referenced_by:
            parts.append("referenced by " + " ".join(
                f"{r['repository']}#{r['number']}" if "repository" in r else describe(r["number"], known, open_issues)
                for r in referenced_by))
        if issue["closingPullRequests"]:
            parts.append("closed by " + " ".join(
                f"#{p['number']}({'merged' if p['merged'] else p['state'].lower()})"
                for p in issue["closingPullRequests"]))
        tags = []
        if issue["labels"]:
            tags.append("[" + ",".join(issue["labels"]) + "]")
        if issue["milestone"]:
            tags.append(f"<{issue['milestone']}>")
        if issue["commentCount"]:
            tags.append(f"{issue['commentCount']} comments")
        head = f"#{issue['number']} | {issue['title']}" + (" " + " ".join(tags) if tags else "")
        print(head)
        for part in parts:
            print(f"    {part}")
    if snapshot["openPullRequests"]:
        print()
        print("## open pull requests")
        for pr in snapshot["openPullRequests"]:
            rel = []
            if pr["closes"]:
                rel.append("closes " + " ".join(f"#{n}" for n in pr["closes"]))
            if pr["mentions"]:
                rel.append("mentions " + " ".join(f"#{n}" for n in pr["mentions"]))
            draft = " (draft)" if pr["isDraft"] else ""
            print(f"#{pr['number']} | {pr['title']}{draft}" + (" | " + "; ".join(rel) if rel else ""))
    if snapshot["unresolvedReferences"]:
        print()
        print("unresolved references (lookup failed or not found): "
              + " ".join(f"#{n}" for n in snapshot["unresolvedReferences"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("repository", nargs="?", help="OWNER/REPO or GitHub URL; defaults to the current checkout's origin")
    parser.add_argument("--out", type=Path, help="output directory (default: a new temporary directory)")
    args = parser.parse_args()

    if shutil.which("gh") is None:
        print("error: GitHub CLI (gh) is required; install and authenticate gh before running this skill", file=sys.stderr)
        return 2

    try:
        repository = resolve_repository(args.repository)
        owner, name = repository.split("/", 1)
        issues = [normalize_issue(node, repository) for node in paginate(ISSUE_QUERY, owner, name, "issues")]
        pull_requests = [normalize_pull_request(node, repository) for node in paginate(PULL_REQUEST_QUERY, owner, name, "pullRequests")]
    except CollectionError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    issues.sort(key=lambda issue: issue["number"])
    pull_requests.sort(key=lambda pr: pr["number"])
    open_numbers = {issue["number"] for issue in issues}
    wanted: set[int] = set()
    for issue in issues:
        wanted.update(issue["mentions"])
        wanted.update(sub["number"] for sub in issue["subIssues"])
        if issue["parent"]:
            wanted.add(issue["parent"])
        wanted.update(ref["number"] for ref in issue["referencedBy"] if "repository" not in ref)
        wanted.update(pr["number"] for pr in issue["closingPullRequests"])
    for pr in pull_requests:
        wanted.update(pr["mentions"])
    wanted -= open_numbers
    wanted -= {pr["number"] for pr in pull_requests}
    resolved, unresolved = resolve_references(owner, name, sorted(wanted))

    snapshot = {
        "repository": repository,
        "collectedAt": datetime.now(UTC).isoformat(timespec="seconds"),
        "openIssues": issues,
        "openPullRequests": pull_requests,
        "references": [resolved[number] for number in sorted(resolved)],
        "unresolvedReferences": sorted(unresolved),
    }

    out_dir = args.out or Path(tempfile.mkdtemp(prefix="issue-roadmap-"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "snapshot.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_issues_markdown(out_dir / "issues.md", snapshot)
    print_index(snapshot, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
