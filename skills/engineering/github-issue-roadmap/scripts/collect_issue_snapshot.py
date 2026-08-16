#!/usr/bin/env python3
"""Collect a read-only snapshot for open-issue roadmap analysis."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REFERENCE = re.compile(r"(?<![\w/])#(\d+)\b")
ISSUE_FIELDS = (
    "number,title,body,author,labels,assignees,milestone,"
    "createdAt,updatedAt,url,comments"
)


class CollectionError(RuntimeError):
    """A concise error safe to show directly to the user."""


def run_gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown gh error"
        raise CollectionError(f"gh {' '.join(args)} failed: {detail}")
    return result.stdout


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

    try:
        repository = run_gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
    except CollectionError as error:
        raise CollectionError(
            "repository was not specified and could not be inferred from the current checkout: "
            f"{error}"
        ) from error
    return repository.strip()


def collect_open_issues(repository: str) -> list[dict[str, Any]]:
    output = run_gh(
        "issue",
        "list",
        "--repo",
        repository,
        "--state",
        "open",
        "--limit",
        "1000",
        "--json",
        ISSUE_FIELDS,
    )
    return json.loads(output)


def referenced_numbers(issues: list[dict[str, Any]]) -> list[int]:
    numbers: set[int] = set()
    for issue in issues:
        texts = [issue.get("body") or ""]
        texts.extend(comment.get("body") or "" for comment in issue.get("comments", []))
        for text in texts:
            numbers.update(int(number) for number in REFERENCE.findall(text))
    return sorted(numbers)


def normalize_open_reference(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": issue["number"],
        "kind": "issue",
        "title": issue["title"],
        "state": "OPEN",
        "closedAt": None,
        "mergedAt": None,
        "url": issue["url"],
    }


def collect_reference(repository: str, number: int) -> dict[str, Any] | None:
    result = subprocess.run(
        ["gh", "api", f"repos/{repository}/issues/{number}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if "HTTP 404" in result.stderr:
            return None
        detail = result.stderr.strip() or result.stdout.strip() or "unknown gh error"
        raise CollectionError(f"could not inspect #{number}: {detail}")

    item = json.loads(result.stdout)
    pull_request = item.get("pull_request")
    return {
        "number": item["number"],
        "kind": "pull_request" if pull_request else "issue",
        "title": item["title"],
        "state": item["state"].upper(),
        "closedAt": item.get("closed_at"),
        "mergedAt": pull_request.get("merged_at") if pull_request else None,
        "url": item["html_url"],
    }


def main() -> int:
    if shutil.which("gh") is None:
        print(
            "error: GitHub CLI (gh) is required; install and authenticate gh before running this skill",
            file=sys.stderr,
        )
        return 2
    if len(sys.argv) > 2:
        print(f"usage: {Path(sys.argv[0]).name} [OWNER/REPO]", file=sys.stderr)
        return 2

    try:
        repository = resolve_repository(sys.argv[1] if len(sys.argv) == 2 else None)
        issues = collect_open_issues(repository)
        open_by_number = {issue["number"]: issue for issue in issues}
        references = []
        for number in referenced_numbers(issues):
            if number in open_by_number:
                references.append(normalize_open_reference(open_by_number[number]))
                continue
            reference = collect_reference(repository, number)
            if reference is not None:
                references.append(reference)
    except (CollectionError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    snapshot = {
        "repository": repository,
        "collectedAt": datetime.now(UTC).isoformat(),
        "openIssueCount": len(issues),
        "openIssues": sorted(issues, key=lambda issue: issue["number"]),
        "references": references,
    }
    json.dump(snapshot, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
