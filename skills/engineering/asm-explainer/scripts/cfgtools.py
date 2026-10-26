"""ISA-independent CFG helpers shared by build.py / validate.py (stdlib only)."""


def dominators(blocks):
    ids = [b["id"] for b in blocks]
    preds = {i: [] for i in ids}
    for b in blocks:
        for s in b.get("successors", []):
            if s.get("target") in preds:
                preds[s["target"]].append(b["id"])
    dom = {i: set(ids) for i in ids}
    if ids:
        dom[ids[0]] = {ids[0]}
    changed = True
    while changed:
        changed = False
        for i in ids[1:]:
            ps = [dom[p] for p in preds[i]]
            new = (set.intersection(*ps) if ps else set()) | {i}
            if new != dom[i]:
                dom[i] = new
                changed = True
    return dom


def relabel_back_edges(data):
    """Mark edges whose target dominates their source as kind 'back'. Returns number relabelled.
    The original kind is kept in 'cond_kind' so taken/not-taken information is not lost."""
    blocks = data.get("blocks", [])
    dom = dominators(blocks)
    n = 0
    for b in blocks:
        for s in b.get("successors", []):
            if s.get("kind") != "back" and s.get("target") in dom.get(b["id"], ()):
                s["cond_kind"] = s["kind"]
                s["kind"] = "back"
                n += 1
    return n
