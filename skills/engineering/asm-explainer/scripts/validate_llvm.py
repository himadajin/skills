"""LLVM IR checks used by validate.py. LLVM is an SSA IR, not an assembly ISA."""
import re

META = re.compile(r",\s*![\w.]+ !\d+")  # metadata attachments (!tbaa, !llvm.loop, !dbg ...)
TERM = r"^(br|ret|switch|unreachable|resume|indirectbr|invoke|callbr)$"


def parse_input(text, fname, norm):
    """-> (values, params, implicit entry label)|None, [normalized text], [None], {label: index}"""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("define") and re.search(rf"@{re.escape(fname.lstrip('@'))}\(", l)), None)
    if start is None: return None, [], [], None
    out, params = [], re.findall(r"%[\w.]+", lines[start].split("(", 1)[1].rsplit(")", 1)[0])
    defs = set(params); labels = {}; entry = None; first = True; pend = None
    for l in lines[start + 1:]:
        if l.startswith("}"): break
        c = META.sub("", l.split(";")[0]).strip()
        if pend is not None:  # continuation of a multi-line instruction (switch [ ... ], indirectbr [ ... ])
            pend += " " + c
            if pend.count("[") <= pend.count("]"): out.append(norm(pend)); pend = None
            continue
        if not c: continue
        m = re.match(r"^([\w.$-]+):", c)
        if m:
            labels[m.group(1)] = len(out); first = False; continue
        if first and entry is None:  # unnamed entry block: implicit label %N (N = number of unnamed params)
            entry = str(sum(1 for q in params if re.fullmatch(r"%\d+", q))) if all(re.fullmatch(r"%\d+", q) for q in params) else None
            entry = entry or "0"
            first = False
        if c.count("[") > c.count("]") and not re.match(r"^(%[\w.]+\s*=\s*)?phi\b", c): pend = c; continue
        out.append(norm(c))
        m = re.match(r"(%[\w.]+)\s*=", c)
        if m: defs.add(m.group(1))
    return (defs, params, entry), out, [None] * len(out), labels


def mnemonic(text):
    t = re.sub(r"^%[\w.]+\s*=\s*", "", text)
    if t.startswith("br "): return "br i1" if t.startswith("br i1") else "br label"
    return t.split()[0]


def is_terminator(mn):
    return bool(re.match(TERM, mn.split()[0]))


def is_return(mn):
    return bool(re.match(r"^(ret|unreachable|resume)$", mn))


def norm_label(label):
    Ln = label.rstrip(":").lstrip("%")
    warn = f"write label as {Ln!r} (no '%' or ':'); accepted" if Ln != label else None
    return Ln, warn


def bind_entry(info, blocks, lab):
    if info and info[2] is not None and not blocks[0].get("label"):
        lab.setdefault(info[2], blocks[0]["id"]); lab.setdefault("%" + info[2], blocks[0]["id"])


def note_seq_mismatch(have, E):
    for t in have:
        if META.search(t): E(f"strip metadata from text: {t[:60]!r}"); break


def expected_successors(b, mn, last, lab, nxt, norm, check_switch, E, W, **_k):
    exp = None
    if mn == "br i1":
        m = re.findall(r"label %([\w.]+)", last)
        if len(m) == 2: exp = [(lab.get(m[0]), "true"), (lab.get(m[1]), "false")]
    elif mn == "br label":
        m = re.findall(r"label %([\w.]+)", last); exp = [(lab.get(m[0]), "jump")]
    elif re.match(r"^(ret|unreachable|resume)$", mn): exp = []
    elif mn == "switch":
        m = re.match(r"switch\s+\S+\s+[^,]+,\s*label\s+%([\w.]+)\s*\[(.*)\]\s*$", norm(last))
        if not m: W(f"{b['id']}: could not parse switch; successors not checked")
        else:
            cases = {}
            for v, t in re.findall(r"\S+\s+(-?\w+),\s*label\s+%([\w.]+)", m.group(2)):
                cases.setdefault(t, []).append(v)
            want_s = [(lab.get(m.group(1)), "default", None)] + [(lab.get(t), "case", frozenset(vs)) for t, vs in cases.items()]
            check_switch(b, b.get("successors", []), want_s, last)
    elif mn in ("indirectbr", "invoke", "callbr"): W(f"{b['id']}: '{mn}' successors not checked")
    else: exp = [(nxt, "fallthrough")] if nxt else []
    for k, (t, _) in enumerate(exp or []):
        if t is None: E(f"{b['id']}: branch label not found among block labels"); exp = None; break
    return exp


def expected_llvm(text, vals):
    """-> defs, uses, phi_incoming[(value, pred_label)]"""
    m = re.match(r"(%[\w.]+)\s*=\s*(.*)$", text)
    d, rest = ([m.group(1)], m.group(2)) if m else ([], text)
    if rest.startswith("phi "):
        return d, [], [(v, p) for v, p in re.findall(r"\[\s*([^,\]]+?)\s*,\s*%([\w.]+)\s*\]", rest)]
    rest = re.sub(r"label %[\w.]+", "", rest)
    u = []
    for v in re.findall(r"%[\w.]+", rest):
        if v in vals and v not in u: u.append(v)
    return d, u, []


def analyze_insn(x, where, extra, lab, b, phi_need, norm, E, W, pending, fn_returns, void_callee):
    vals = extra[0] if extra else set()
    Dl, Ul = list(x.get("defs", [])), list(x.get("uses", []))
    for r in Dl + Ul:
        if r not in vals: E(f"{where}: {r} is not a value of this function")
    ed, eu_, inc = expected_llvm(norm(x.get("text", "")), vals)
    if inc:
        if Ul: E(f"{where}: phi uses must be [] (operands go in edge_uses), found {Ul}")
        for v, p in inc:
            if v in vals and p in lab: phi_need.add((lab[p], b["id"], v))
        Ul = []
    return ed, eu_, [], "", [], Ul


def why(_cls, _md, _text):
    return ""


def finish_phi(eu, phi_need, E):
    for fr, to, v in sorted(phi_need):
        if v not in eu.get((fr, to), set()): E(f"edge_uses {fr}->{to}: must include {v} (phi in {to})")
    have_eu = {(fr, to, v) for (fr, to), vs in eu.items() for v in vs}
    for fr, to, v in sorted(have_eu - phi_need): E(f"edge_uses {fr}->{to}: {v} is not a phi operand on that edge")


def check_roles(listed, extra, ret_used, live_in, f, T, blocks, E, W):
    params = extra[1] if extra else []
    for n, r in listed.items():
        role = r.get("role")
        if n in params and role not in ("argument", "argument+return"): W(f"registers.{n}: function parameter -> role argument")
        if n not in params and role in ("argument", "argument+return"): W(f"registers.{n}: not a parameter -> role ssa-value or return")
        if n not in params and n in ret_used and role != "return": W(f"registers.{n}: value given to ret -> role return (even if it is also a phi/loop value)")
        if n in params and n in ret_used and role == "argument": E(f"registers.{n}: parameter returned by ret -> role argument+return")


def target():
    return dict(
        parse=parse_input, mnemonic=mnemonic, is_term=is_terminator, is_return=is_return,
        norm_label=norm_label, bind_entry=bind_entry, note_seq_mismatch=note_seq_mismatch,
        check_labels=lambda **_k: None, require_case_value=True, successors=expected_successors,
        analyze_insn=analyze_insn, why=why, check_source_line=False, finish_phi=finish_phi,
        check_roles=check_roles,
    )
