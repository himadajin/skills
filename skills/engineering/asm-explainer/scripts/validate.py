#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Validate an asm-explainer JSON against its input.
  python3 validate.py data.json input.(s|ll) [--isa riscv|aarch64|llvm]
One short line per problem, written for an LLM fixing its own JSON. Exit 1 if any ERROR.
Core is ISA-independent; per-ISA knowledge lives in the small tables below (stdlib only)."""
import json, re, sys, difflib, argparse, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfgtools import dominators

# ============================ per-ISA tables ============================
RV_ABI = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1"] + [f"a{i}" for i in range(8)] + \
         [f"s{i}" for i in range(2, 12)] + ["t3", "t4", "t5", "t6"]
RV_FABI = [f"ft{i}" for i in range(8)] + ["fs0", "fs1"] + [f"fa{i}" for i in range(8)] + \
          [f"fs{i}" for i in range(2, 12)] + [f"ft{i}" for i in range(8, 12)]
RV_ALIAS = {**{f"x{i}": n for i, n in enumerate(RV_ABI)}, **{f"f{i}": n for i, n in enumerate(RV_FABI)}, "fp": "s0"}
RV_CANON = set(RV_ABI) | set(RV_FABI)
A64_ALIAS = {**{f"w{i}": f"x{i}" for i in range(31)}, **{f"{p}{i}": f"v{i}" for p in "bhsdq" for i in range(32)},
             "wzr": "xzr", "wsp": "sp", "lr": "x30", "fp": "x29"}
A64_CANON = {f"x{i}" for i in range(31)} | {f"v{i}" for i in range(32)} | {"sp", "xzr", "nzcv"}

ISA = {
 "riscv": dict(alias=RV_ALIAS, canon=RV_CANON, zero={"zero"}, comment="#", flags=None,
   ra="ra", ret_regs=["a0", "a1", "fa0", "fa1"], fixed={"sp": "stack-pointer", "ra": "return-address"},
   args={f"a{i}" for i in range(8)} | {f"fa{i}" for i in range(8)},
   caller_saved=set(f"a{i}" for i in range(8)) | {f"t{i}" for i in range(7)} | {f"ft{i}" for i in range(12)} | {f"fa{i}" for i in range(8)},
   cond=r"^(c\.)?b(eq|ne|lt|ge|ltu|geu|eqz|nez|lez|gez|ltz|gtz|gt|le|gtu|leu)z?$", jump=r"^(c\.)?j$", ret=r"^(c\.)?ret$",
   classes=[  # (class, mnemonic regex) first match wins
     ("store", r"^(c\.)?(s[bhwd]|fs[wdh]|c\.s[wd]sp|c\.fs[wd]sp?)$"),
     ("branch", r"^(c\.)?b\w+$"), ("none", r"^(c\.)?(j|nop|fence(\.i)?|ecall|ebreak|unimp)$"),
     ("ret", r"^(c\.)?ret$"), ("jr", r"^(c\.)?jr$"), ("call", r"^(call|jal|c\.jal)$"), ("tail", r"^tail$"),
     ("jalr", r"^(c\.)?jalr$"), ("rmw", r"^c\.(add|addi|sub|and|or|xor|slli|srli|srai|andi|addw|subw|addiw)$"),
     ("csr", r"^csr\w+$"), ("alu", r".")]),
 "aarch64": dict(alias=A64_ALIAS, canon=A64_CANON, zero={"xzr"}, comment="//", flags="nzcv",
   ra="x30", ret_regs=["x0", "x1", "v0", "v1"], fixed={"sp": "stack-pointer", "x30": "return-address", "nzcv": "flags"},
   args={f"x{i}" for i in range(8)} | {f"v{i}" for i in range(8)},
   caller_saved={f"x{i}" for i in range(18)} | {f"v{i}" for i in list(range(8)) + list(range(16, 32))} | {"nzcv"},
   cond=r"^(b\.\w+|cbn?z|tbn?z)$", jump=r"^b$", ret=r"^ret$",
   classes=[
     ("storepair", r"^st(n?p)$"), ("storex", r"^stl?xr[bh]?$|^stl?xp$"),
     ("store", r"^(st(r|ur|lr|llr)[bh]?|st[1-4])$"),
     ("loadpair", r"^ld(n?p|psw|axp|xp)$"), ("load", r"^ld(r|ur|ar|apr|xr|axr|lar)(s?[bhw])?$|^ld[1-4]r?$|^prfu?m$"),
     ("cmp", r"^(cmp|cmn|tst|fcmpe?)$"), ("ccmp", r"^(ccmp|ccmn|fccmpe?)$"),
     ("bcond", r"^b\.\w+$"), ("cbz", r"^(cbn?z|tbn?z)$"), ("none", r"^(b|nop|isb|dmb|dsb|hint|brk|udf|svc)$"),
     ("call", r"^blr?$"), ("ret", r"^ret$"), ("br", r"^br$"),
     ("cset", r"^(cset|csetm)$"), ("readflags", r"^(csel|csinc|csinv|csneg|cinc|cinv|cneg|fcsel|adc|sbc|ngc)$"),
     ("rwflags", r"^(adcs|sbcs|ngcs)$"), ("setflags", r"^(subs|adds|ands|bics|negs)$"),
     ("rmw", r"^(movk|bfi|bfxil|bfm|mla|mls|fmla|fmls|ins|sli|sri|sdot|udot|bsl|bit|bif|tbx)$"),
     ("alu", r".")]),
 "llvm": dict(alias={}, canon=None, zero=set(), comment=";", flags=None, ra=None, ret_regs=[], fixed={}, caller_saved=set(),
   cond=r"^br i1$", jump=r"^br label$", ret=r"^(ret|unreachable|resume)$", classes=[]),
}
WHY = {"store": "store: every register operand is read", "cmp": "compare: writes only flags",
       "setflags": "flag-setting op: writes nzcv", "bcond": "conditional branch reads nzcv", "readflags": "reads nzcv",
       "call": "call writes the return-address register", "ret": "ret reads the return-address register",
       "rmw": "destination is also read (read-modify-write)", "storepair": "store pair: every register operand is read",
       "loadpair": "load pair: both destinations are written", "cset": "cset reads nzcv", "ccmp": "ccmp/ccmn/fccmp: operands are read only; nzcv is read and written"}

# ============================ input parsing ============================
META = re.compile(r",\s*![\w.]+ !\d+")  # LLVM metadata attachments (!tbaa, !llvm.loop, !dbg ...)


def detect_isa(isa_field, path):
    s = (isa_field or "").lower()
    if path.endswith(".ll") or "llvm" in s: return "llvm"
    if "aarch64" in s or "arm" in s: return "aarch64"
    return "riscv"


def norm(t):
    t = re.sub(r"\s+", " ", t.strip())
    return re.sub(r"\s*,\s*", ", ", t)


def input_insns(text, fname, isa):
    """-> (llvm (values, params, implicit entry label)|None, [normalized text], [source line or None],
           {label: index of the next instruction})"""
    lines = text.splitlines()
    if isa == "llvm":
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
    start = next((i for i, l in enumerate(lines) if re.match(rf"^{re.escape(fname)}:", l)), None)
    if start is None: return None, [], [], None
    out, locs, loc, labels = [], [], None, {fname: 0}
    locpos = None; lastlab = 0  # index of the first instruction after the latest .loc / after the latest block label
    for l in lines[start + 1:]:
        if re.match(r"^\.Lfunc_end\d+:", l) or re.match(r"\s*\.(size|cfi_endproc)\b", l) or re.match(r"^[A-Za-z_][\w.$]*:", l):
            break
        m = re.match(r"\s*\.loc\s+\d+\s+(\d+)", l)
        if m: loc = int(m.group(1)) or None; locpos = len(out); continue
        m = re.match(r"^\s*([\w.$]+):", l)
        if m:
            labels[m.group(1)] = len(out)
            if re.match(r"^\.L(BB[\w$]+|\d+)$", m.group(1)): lastlab = len(out)  # branch-target label: L1 boundary
        c = re.sub(r"^\s*[\w.$]+:", "", l.split(ISA[isa]["comment"])[0]).strip()
        if not c or c.startswith("."): continue
        out.append(norm(c)); locs.append(loc if locpos is not None and locpos >= lastlab else None)  # L1: no carry across a label
    return None, out, locs, labels


DIRECTIVE = re.compile(r"^\s*\.(word|long|quad|xword|dword|4byte|8byte|2byte|hword|short|half|byte)\s+(.*)$")


def jump_table(text, label):
    """entries of a jump table '<label>:' followed by data directives -> [target label] or None"""
    lines = text.splitlines()
    i = next((k for k, l in enumerate(lines) if re.match(rf"^\s*{re.escape(label)}:", l)), None)
    if i is None: return None
    out = []
    for l in lines[i + 1:]:
        c = l.split("//")[0].split("#")[0].strip()
        if not c or c.startswith((".p2align", ".align")): continue
        m = DIRECTIVE.match(c)
        if not m: break
        labs = [t for t in re.findall(r"\.?[A-Za-z_$][\w.$]*", m.group(2)) if t != label]
        if not labs: return None
        out.append(labs[0])
    return out or None


def mnemonic(text, isa):
    if isa == "llvm":
        t = re.sub(r"^%[\w.]+\s*=\s*", "", text)
        if t.startswith("br "): return "br i1" if t.startswith("br i1") else "br label"
        return t.split()[0]
    return text.split()[0].lower()


def split_ops(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "[(": depth += 1
        if ch in "])": depth -= 1
        if ch == "," and depth == 0: out.append(cur.strip()); cur = ""
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return out


IMM = [re.compile(r"%[\w.]+\([^()]*\)"),               # relocations %hi(x) %pcrel_lo(.L) %lo(sym)
       re.compile(r":[\w]+:[\w.$+-]+"),                  # :lo12:sym  :got:sym
       re.compile(r"#\s*[-+]?[\w.+-]*"),                   # #imm  #0x10  #-1  #1.0e+00
       re.compile(r"(?<![\w.])[-+]?(0x[0-9a-fA-F]+|\d[\w.]*)"),  # bare literals 0x10, 16, 0(a0)
       re.compile(r"\b(lsl|lsr|asr|ror|msl|[us]xt[bhwx])\b", re.I)]   # shift / extend keywords


def strip_imm(op):
    for rx in IMM: op = rx.sub(" ", op)
    return op


def regs_in(op, T):
    """canonical register names in one operand (zero regs dropped), in order; immediates/relocations ignored"""
    out = []
    for t in re.findall(r"[A-Za-z][\w]*", strip_imm(re.sub(r"\.\d*[bhsdq]\b", "", op))):
        c = T["alias"].get(t.lower(), t.lower())
        if c in T["canon"] and c not in T["zero"] and c not in out: out.append(c)
    return out


def expected_asm(text, isa, T, fn_returns):
    """-> (defs, uses, optional_uses, cls) using the mnemonic-class table. optional = may be listed, not required."""
    parts = text.split(None, 1); mn = parts[0].lower(); ops = split_ops(parts[1]) if len(parts) > 1 else []
    cls = next(c for c, rx in T["classes"] if re.match(rx, mn))
    if cls == "jr" and ops and T["alias"].get(ops[0], ops[0]) == "ra": cls = "ret"  # jr ra == ret
    R = [regs_in(o, T) for o in ops]; flat = [r for rs in R for r in rs]
    D, U, OPT = [], [], []
    wb_base = None  # pre/post-index writeback
    if isa == "aarch64":
        for k, o in enumerate(ops):
            if o.startswith("[") and (o.endswith("!") or (k + 1 < len(ops) and not ops[k + 1].startswith("["))) and cls in ("load", "loadpair", "store", "storepair"):
                if o.endswith("!") or re.match(r"^#?-?\w+$", ops[k + 1]) and k + 1 == len(ops) - 1: wb_base = regs_in(o, T)[0] if regs_in(o, T) else None
    if cls in ("store", "storepair", "branch", "cmp", "cbz", "jr", "br"):
        U = flat
    elif cls == "storex":       # stxr ws, xt, [xn]
        D, U = R[0], [r for rs in R[1:] for r in rs]
    elif cls == "loadpair":
        D, U = R[0] + R[1], [r for rs in R[2:] for r in rs]
    elif cls == "rmw":
        D, U = R[0], R[0] + [r for rs in R[1:] for r in rs]
    elif cls == "none" or cls == "csr" and not ops:
        pass
    elif cls == "call":
        if isa == "riscv" and mn == "jal" and len(ops) == 2: D = R[0]
        else: D = [T["ra"]]
        U = flat if isa == "aarch64" else []
        OPT = list(T["caller_saved"])
        D_opt = [T["ret_regs"][0]]
        return D, U, OPT, cls, D_opt
    elif cls == "tail":
        U = []; OPT = list(T["caller_saved"]) + ["ra"]
    elif cls == "jalr":
        if len(ops) == 1: D, U = ["ra"], R[0]
        else: D, U = R[0], [r for rs in R[1:] for r in rs]
    elif cls == "ret":
        U = flat or [T["ra"]]
        OPT = list(T["ret_regs"])
    elif cls == "cset":
        D, U = R[0], []
    elif cls == "ccmp":         # ccmp/ccmn/fccmp: compare only; operands are read, nzcv read+written (below)
        D, U = [], flat
    else:  # alu / load / readflags / setflags / csr: first operand written, the rest read
        D = R[0] if R else []
        U = [r for rs in R[1:] for r in rs]
    if wb_base and wb_base not in D: D = D + [wb_base]
    if T["flags"]:
        if cls in ("cmp", "setflags", "rwflags", "ccmp"): D = D + [T["flags"]]
        if cls in ("bcond", "readflags", "cset", "rwflags", "ccmp"): U = U + [T["flags"]]
    return D, U, OPT, cls, []


LLVM_TERM = r"^(br|ret|switch|unreachable|resume|indirectbr|invoke|callbr)$"


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


# ============================ main ============================
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("json"); ap.add_argument("input"); ap.add_argument("--isa")
    ap.add_argument("--source", help=".c or .ll with the callee prototypes (to know which calls return void)")
    a = ap.parse_args()
    d = json.load(open(a.json)); src = open(a.input, encoding="utf-8", errors="replace").read()
    proto = open(a.source, encoding="utf-8", errors="replace").read() if a.source else ""
    if a.input.endswith(".ll"): proto += "\n" + src

    def void_callee(text):
        m = re.match(r"^\s*(call|bl|jal|tail)\s+([\w.$]+)", text)
        if not m or not proto: return False
        n = re.escape(m.group(2).split("@")[0])
        return bool(re.search(rf"(declare|define)\s[^@\n]*\bvoid\s+@{n}\(|\bvoid\s+\**\s*{n}\s*\(", proto))
    errs, warns = [], []
    E, W = errs.append, warns.append
    f = d.get("function") or {}
    for k in ("name", "isa"):
        if not f.get(k): E(f"function.{k}: missing")
    if not isinstance(d.get("blocks"), list) or not d["blocks"]: E("blocks: missing/empty"); return report(errs, warns)
    isa = a.isa or detect_isa(f.get("isa"), a.input); T = ISA[isa]
    blocks = d["blocks"]; ids = [b.get("id") for b in blocks]; byid = {b.get("id"): b for b in blocks}
    if len(set(ids)) != len(ids): E("blocks: duplicate id")
    for b in blocks:
        for k in ("id", "instructions", "successors"):
            if k not in b: E(f"block {b.get('id')}: missing {k}")
        for j, x in enumerate(b.get("instructions", [])):
            for k in ("text", "defs", "uses"):
                if k not in x: x.setdefault(k, []); E(f"{b.get('id')}[{j}]: missing {k}")
    ROLES = {"argument", "return", "argument+return", "callee-saved", "temporary", "return-address", "stack-pointer",
             "frame-pointer", "zero", "flags", "ssa-value", "other", "undefined-live-in"}
    for i, r in enumerate(d.get("registers", [])):
        if not r.get("name") or not r.get("role"): E(f"registers[{i}]: needs name and role")
        elif r["role"] not in ROLES: E(f"registers.{r['name']}: role {r['role']!r} not in enum")
    # ---- (1) verbatim instruction sequence
    llvm_info, want, locs, labpos = input_insns(src, f.get("name", ""), isa)
    have = [norm(x.get("text", "")) for b in blocks for x in b.get("instructions", [])]
    seq_ok = bool(want) and have == want
    if not want: E(f"input: function {f.get('name')} not found")
    elif not seq_ok:
        for t in have:
            if isa == "llvm" and META.search(t): E(f"strip metadata from text: {t[:60]!r}"); break
        sm = difflib.SequenceMatcher(a=want, b=have, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal": continue
            if op == "delete": E(f"missing instr after #{j1 - 1}: {want[i1:i2][:3]}")
            elif op == "insert": E(f"extra instr #{j1}..#{j2 - 1} (not in input): {have[j1:j2][:3]}")
            else: E(f"instr #{j1}..#{j2 - 1} differ: json {have[j1:j2][:2]} vs input {want[i1:i2][:2]}")
    # ---- (2) block boundaries + successors derived from the terminator
    lab = {}
    for b in blocks:
        L0 = b.get("label")
        if L0:
            Ln = L0.rstrip(":").lstrip("%") if isa == "llvm" else L0.rstrip(":")
            if Ln != L0: W(f"{b['id']}: write label as {Ln!r} (no '%' or ':'); accepted")
            lab[Ln] = b["id"]; lab["%" + Ln] = b["id"]
    if isa == "llvm" and llvm_info and llvm_info[2] is not None and not blocks[0].get("label"):
        lab.setdefault(llvm_info[2], blocks[0]["id"]); lab.setdefault("%" + llvm_info[2], blocks[0]["id"])
    # B3: labelled blocks must start at that label; branch/table targets must start a block
    if seq_ok and labpos is not None and isa != "llvm":
        starts, g = {}, 0
        for b in blocks: starts[b["id"]] = g; g += len(b.get("instructions", []))
        for b in blocks:
            L0 = b.get("label")
            if not L0: continue
            if L0 not in labpos: E(f"{b['id']}: label {L0!r} not found in the input")
            elif labpos[L0] != starts[b["id"]]: E(f"{b['id']}: label {L0!r} is at instruction #{labpos[L0]} in the input, block starts at #{starts[b['id']]}")
            elif re.match(r"^\.L(pcrel_hi|tmp|func_begin|func_end)", L0): E(f"{b['id']}: {L0} is not a branch target; it does not start a block (B3)")
        refd = set(re.findall(r"\.L(?:BB[\w$]+|\d+)\b", " ".join(want)))
        for jl in set(re.findall(r"\.LJTI[\w$]+", " ".join(want))): refd |= set(jump_table(src, jl) or [])
        bystart = {v: k for k, v in starts.items()}
        for L0 in sorted(refd):
            if L0 in labpos and not any(b.get("label") == L0 for b in blocks):
                E(f"label {L0} is a branch/jump-table target: it must start a block with label {L0!r}")
    DOM = dominators(blocks)

    def cv(s):
        c = s.get("case")
        return None if c is None else frozenset(str(v) for v in (c if isinstance(c, list) else [c]))

    def check_switch(b, succ, want_s, last):
        """want_s: [(target, kind, frozenset(case values) | None=unchecked)]"""
        got = [(s.get("target"), s.get("cond_kind", s.get("kind")) if s.get("kind") == "back" else s.get("kind"), cv(s)) for s in succ]
        rem = list(got)
        for t, k, vs in want_s:
            hit = next((g for g in rem if g[0] == t and g[1] == k and (vs is None or g[2] == vs)), None)
            if hit: rem.remove(hit); continue
            near = next((g for g in rem if g[0] == t), None)
            if near and near[1] != k: E(f"{b['id']}: edge to {t} should be kind {k!r} (found {near[1]!r})"); rem.remove(near)
            elif near: E(f"{b['id']}: case edge to {t} should have case {sorted(vs)} (found {sorted(near[2] or [])})"); rem.remove(near)
            else: E(f"{b['id']}: needs successor {{target:{t}, kind:{k}" + (f", case:{sorted(vs)}" if vs else "") + f"}} (from '{last[:60]}')")
        for g in rem: E(f"{b['id']}: unexpected successor {{target:{g[0]}, kind:{g[1]}}} (not a target of '{last[:60]}')")
    def is_term(mn):
        if isa == "llvm": return bool(re.match(LLVM_TERM, mn.split()[0]))
        return bool(re.match(T["cond"], mn) or re.match(T["jump"], mn) or re.match(T["ret"], mn) or mn in ("br", "jr", "c.jr", "tail"))
    for i, b in enumerate(blocks):
        ins = b.get("instructions", []); succ = b.get("successors", []); nxt = ids[i + 1] if i + 1 < len(ids) else None
        for s in succ:
            if s.get("target") not in byid: E(f"{b['id']}: successor target {s.get('target')!r} does not exist")
            if s.get("kind") not in ("true", "false", "jump", "fallthrough", "back", "case", "default"): E(f"{b['id']}: successor kind {s.get('kind')!r} invalid")
            if s.get("kind") == "case" and s.get("case") in (None, "", []) and isa == "llvm": E(f"{b['id']}: case edge to {s.get('target')} needs a 'case' value")
            if s.get("kind") != "case" and "case" in s and s.get("kind") != "back": E(f"{b['id']}: 'case' field only on kind 'case' edges")
        if not ins: W(f"{b['id']}: empty block"); continue
        for j, x in enumerate(ins[:-1]):
            if is_term(mnemonic(x["text"], isa)):
                E(f"{b['id']}[{j}]: '{mnemonic(x['text'], isa)}' ends a block; start a new block after it")
        last = ins[-1]["text"]; mn = mnemonic(last, isa)
        tgts = [lab[t] for t in re.findall(r"%?[\w.$]+", re.sub(r"^\S+", "", last) if isa != "llvm" else last) if t in lab]
        exp = None  # list of (target, kind)
        if isa == "llvm":
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
                    check_switch(b, succ, want_s, last)
            elif mn in ("indirectbr", "invoke", "callbr"): W(f"{b['id']}: '{mn}' successors not checked")
            else: exp = [(nxt, "fallthrough")] if nxt else []
            for k, (t, _) in enumerate(exp or []):
                if t is None: E(f"{b['id']}: branch label not found among block labels"); exp = None; break
        elif re.match(T["cond"], mn):
            exp = [(tgts[-1] if tgts else None, "true"), (nxt, "false")]
            if not tgts: E(f"{b['id']}: branch target of '{last}' is not a block label"); exp = None
        elif re.match(T["jump"], mn):
            exp = [(tgts[-1], "jump")] if tgts else None
            if not tgts: E(f"{b['id']}: jump target of '{last}' is not a block label")
        elif re.match(T["ret"], mn) or mn == "tail" or (isa == "riscv" and re.match(r"^(c\.)?jr (ra|x1)$", norm(last))): exp = []
        elif mn in ("br", "jr", "c.jr"):
            jt = b.get("jump_table")
            jls = sorted(set(re.findall(r"\.LJTI[\w$]+", " ".join(want))))
            if not jt and jls: E(f"{b['id']}: indirect jump '{last}' with jump table {jls[0]} in the function: add jump_table {{label, targets}} and case successors")
            elif not jt: W(f"{b['id']}: indirect jump '{last}': successors not checked (add jump_table if it jumps through a table)")
            else:
                ent = jump_table(src, jt.get("label", "")) if jt.get("label") else None
                if not jt.get("label") or jt["label"] not in " ".join(want): E(f"{b['id']}: jump_table.label {jt.get('label')!r} is not referenced in the function")
                if ent is None: W(f"{b['id']}: could not parse jump table {jt.get('label')!r} in the input; successors not checked")
                else:
                    tl = [lab.get(e) for e in ent]
                    if None in tl: E(f"{b['id']}: jump table entry {ent[tl.index(None)]} is not a block label")
                    jtt = [t.get("target") if isinstance(t, dict) else t for t in jt.get("targets", [])]
                    if jtt != tl: E(f"{b['id']}: jump_table.targets should be {tl} (table order, one per entry; found {jtt})")
                    vals_by_t = {}
                    for t in jt.get("targets", []):
                        if isinstance(t, dict) and t.get("case") is not None: vals_by_t.setdefault(t.get("target"), set()).update(map(str, t["case"] if isinstance(t["case"], list) else [t["case"]]))
                    want_s = [(t, "case", frozenset(vals_by_t[t]) if t in vals_by_t else None) for t in dict.fromkeys(tl) if t]
                    check_switch(b, succ, want_s, last)
        else: exp = [(nxt, "fallthrough")] if nxt else []
        if exp is not None:
            got = [(s.get("target"), s.get("kind")) for s in succ]; rem = list(got)
            for t, k in exp:
                hit = next((g for g in rem if g == (t, k)), None) or next((g for g in rem if g == (t, "back")), None)
                if hit: rem.remove(hit)
                else: E(f"{b['id']}: needs successor {{target:{t}, kind:{k}}} (from '{last}')" if t else f"{b['id']}: '{last}' falls off the end of the function")
            for g in rem: E(f"{b['id']}: unexpected successor {{target:{g[0]}, kind:{g[1]}}}; '{last}' gives {[{'target': t, 'kind': k} for t, k in exp]}")
        for s in succ:
            if s.get("kind") == "back" and s.get("target") not in DOM.get(b["id"], ()):
                E(f"{b['id']}: edge to {s.get('target')} is not a back-edge (target does not dominate); use its branch kind")
        if any(s.get("kind") == "back" for s in succ):
            W(f"{b['id']}: kind 'back' is computed by build.py; write true/false/jump/fallthrough instead")
    # ---- (3) defs/uses per instruction
    listed = {r.get("name"): r for r in d.get("registers", [])}
    eu = {}
    for e in d.get("edge_uses", []) or []:
        if e.get("from") not in byid or e.get("to") not in byid: E(f"edge_uses {e.get('from')}->{e.get('to')}: unknown block")
        elif e["to"] not in [s.get("target") for s in byid[e["from"]].get("successors", [])]: E(f"edge_uses {e['from']}->{e['to']}: not a CFG edge")
        eu.setdefault((e.get("from"), e.get("to")), set()).update(e.get("uses", []))
    phi_need = set()
    vals, params = (llvm_info or (set(), [], None))[:2]
    gi = 0; bstart = {}
    for b in blocks: bstart[b["id"]] = gi; gi += len(b.get("instructions", []))
    gi = 0
    for b in blocks:
        pending = {}  # argument register -> read since written? (written in this block since the last call)
        for j, x in enumerate(b.get("instructions", [])):
            where = f"{b['id']}[{j}] '{x.get('text', '')[:48]}'"
            gi += 1; L = locs[gi - 1] if seq_ok and gi - 1 < len(locs) else None
            Dl, Ul, Cl = list(x.get("defs", [])), list(x.get("uses", [])), list(x.get("clobbers", []) or [])
            if isa == "llvm":
                for r in Dl + Ul:
                    if r not in vals: E(f"{where}: {r} is not a value of this function")
                ed, eu_, inc = expected_llvm(norm(x.get("text", "")), vals)
                ed_opt = []
                if inc:
                    if Ul: E(f"{where}: phi uses must be [] (operands go in edge_uses), found {Ul}")
                    for v, p in inc:
                        if v in vals and p in lab: phi_need.add((lab[p], b["id"], v))
                    Ul = []
                opt = []
            else:
                bad = False
                for r in Dl + Ul + Cl:
                    c = T["alias"].get(r, r)
                    if c != r: E(f"{where}: write canonical {c} instead of {r} (text keeps {r})"); bad = True
                    elif r in T["zero"]: E(f"{where}: zero register {r} must not appear in defs/uses"); bad = True
                    elif r not in T["canon"]: E(f"{where}: unknown register {r!r}"); bad = True
                if bad: continue
                L = L
                ed, eu_, opt, cls, ed_opt = expected_asm(x.get("text", ""), isa, T, f.get("returns"))
                if cls in ("call", "tail"):
                    # D6 call arguments. An argument register written since the last call (same block) and not read
                    # before the call is dead unless the callee reads it (the call clobbers it) -> ERROR.
                    # One that was also read in between may be scratch -> warn only.
                    dead = sorted(r for r, rd in pending.items() if not rd and r not in Ul)
                    rd_ = sorted(r for r, rd in pending.items() if rd and r not in Ul)
                    if dead: E(f"{where}: {dead} written since the last call and not read before it -> it is an argument: add to uses")
                    if rd_: W(f"{where}: {rd_} set up before the call -> add to uses if it is an argument")
                    if not Cl: W(f"{where}: no clobbers; list caller-saved regs it destroys (else liveness runs through the call)")
                    pending = {}
                else:
                    for r in Ul:
                        if r in pending: pending[r] = True
                    for r in set(Dl) & T["args"]: pending[r] = False
                cr = x.get("callee_returns") or (void_callee(x.get("text", "")) and "void")
                if cls == "call" and cr == "void" and T["ret_regs"][0] in Dl:
                    E(f"{where}: callee returns void -> {T['ret_regs'][0]} goes in clobbers, not defs")
                elif cls == "call" and cr != "void" and not any(r in Dl for r in T["ret_regs"]):
                    W(f"{where}: call should also def return register {T['ret_regs'][0]} (if the callee returns void, set \"callee_returns\": \"void\")")
                if cls == "ret" and f.get("returns") and isa != "llvm":
                    rl = T["alias"].get(f["returns"].get("location", ""), f["returns"].get("location", ""))
                    if rl in T["canon"] and rl not in Ul: E(f"{where}: ret must also use the return register {rl}")
                for c in Cl:
                    if c not in T["caller_saved"]: E(f"{where}: clobbers {c} is not caller-saved")
            md = [r for r in ed if r not in Dl]; xd = [r for r in Dl if r not in ed and r not in ed_opt]
            mu = [r for r in eu_ if r not in Ul]; xu = [r for r in Ul if r not in eu_ and r not in opt]
            why = WHY.get(cls, "") if isa != "llvm" else ""
            if md and isa == "aarch64" and any(re.search(rf"\[[wx]?{re.escape(r[1:])}\b|\[{r}\b", x.get("text", "")) for r in md):
                why = "pre/post-index writeback ([base, #i]! or [base], #i) also writes the base"
            if md or xd: E(f"{where}: defs should be {ed + [r for r in Dl if r in ed_opt]} (found {Dl})" + (f"; {why}" if why else ""))
            if mu or xu: E(f"{where}: uses should be {eu_ + [r for r in Ul if r in opt]} (found {Ul})" + (f"; {why}" if why else ""))
            for r in Dl + Ul:
                if r not in listed: W(f"{b['id']}[{j}]: {r} not in registers[] (not plotted)")
            # source_line vs .loc
            if seq_ok and isa != "llvm":
                s = x.get("source_line")
                if L and s and s != L: E(f"{b['id']}[{j}]: source_line {s} but .loc says {L}")
                elif L and not s: W(f"{b['id']}[{j}]: .loc says line {L}; set source_line")
                elif s and not L: W(f"{b['id']}[{j}]: source_line {s} but .loc says 0/none; omit it")
    if isa == "llvm":
        for fr, to, v in sorted(phi_need):
            if v not in eu.get((fr, to), set()): E(f"edge_uses {fr}->{to}: must include {v} (phi in {to})")
        have_eu = {(fr, to, v) for (fr, to), vs in eu.items() for v in vs}
        for fr, to, v in sorted(have_eu - phi_need): E(f"edge_uses {fr}->{to}: {v} is not a phi operand on that edge")
    # ---- (4) roles (heuristic -> warn)
    live_in = entry_live_in(blocks, eu)
    retloc = (f.get("returns") or {}).get("location")
    retloc = T["alias"].get(retloc, retloc) if retloc else None
    ret_used = set()
    for b in blocks:
        for x in b.get("instructions", []):
            if re.match(T["ret"], mnemonic(x.get("text", ""), isa)): ret_used |= set(x.get("uses", []))
    fp_set = None  # frame pointer set from sp in the prologue (mov x29, sp / add x29, sp, #n / addi s0, sp, n)
    fpreg = {"aarch64": "x29", "riscv": "s0"}.get(isa)
    for x in (blocks[0].get("instructions", []) + (blocks[1].get("instructions", []) if len(blocks) > 1 else [])):
        if fpreg and x.get("defs") == [fpreg] and x.get("uses") == ["sp"] and re.match(r"^(mov|add|addi|c\.addi4spn)\s", norm(x.get("text", ""))): fp_set = x.get("text")
    CALLEE = {"aarch64": {f"x{i}" for i in range(19, 29)} | {f"v{i}" for i in range(8, 16)},
              "riscv": {f"s{i}" for i in range(12)} | {f"fs{i}" for i in range(12)}}.get(isa, set())
    for n, r in listed.items():
        role = r.get("role")
        if isa == "llvm":
            if n in params and role not in ("argument", "argument+return"): W(f"registers.{n}: function parameter -> role argument")
            if n not in params and role in ("argument", "argument+return"): W(f"registers.{n}: not a parameter -> role ssa-value or return")
            if n not in params and n in ret_used and role != "return": W(f"registers.{n}: value given to ret -> role return (even if it is also a phi/loop value)")
            if n in params and n in ret_used and role == "argument": E(f"registers.{n}: parameter returned by ret -> role argument+return")
            continue
        if n == retloc and n in live_in and n in ret_used and role in ("argument", "return"):
            E(f"registers.{n}: holds a parameter on entry and is the return register read by ret -> role argument+return")
        if n == fpreg and fp_set and role != "frame-pointer":
            E(f"registers.{n}: set from sp in the prologue ('{fp_set}') -> role frame-pointer")
        if n in CALLEE and n in live_in and role in ("temporary", "other", "return") and not (n == fpreg and fp_set):
            E(f"registers.{n}: callee-saved register live at entry (saved/restored) -> role callee-saved, not {role}")
        fx = T["fixed"].get(n)
        if fx and role != fx: W(f"registers.{n}: role should be {fx}")
        if n == "x29" and role not in ("frame-pointer", "callee-saved"): W(f"registers.{n}: role frame-pointer (or callee-saved)")
        ploc = {T["alias"].get(p.get("location"), p.get("location")) for p in f.get("params", [])}
        if n in live_in and role in ("temporary", "other", "zero", "return") and (n in ploc or n in CALLEE or n in T["fixed"]):
            W(f"registers.{n}: read before any write (live at entry) -> role argument / callee-saved, not {role}")
        elif n in live_in and role in ("temporary", "zero", "return"):
            W(f"registers.{n}: read before any write but not a parameter location -> role undefined-live-in (if the code really reads an undefined value) or check defs/uses")
        if role == "undefined-live-in" and n not in live_in: W(f"registers.{n}: role undefined-live-in but never read before written")
        if role == "undefined-live-in" and (n in ploc or n in CALLEE): W(f"registers.{n}: is a parameter location / callee-saved -> role argument / callee-saved")
        if role in ("argument", "argument+return") and n not in live_in and n not in [T["alias"].get(p.get("location"), p.get("location")) for p in f.get("params", [])]:
            W(f"registers.{n}: role {role} but never read before written")
    for p in f.get("params", []):
        loc = T["alias"].get(p.get("location"), p.get("location"))
        if loc and loc not in listed: W(f"function.params {p.get('name')}: location {loc} not in registers[]")
    # ---- (5) empty prose
    empty = []
    if not f.get("summary"): empty.append("function.summary")
    for b in blocks:
        for k in ("summary", "explanation"):
            if not b.get(k): empty.append(f"{b['id']}.{k}")
        empty += [f"{b['id']}[{j}].note" for j, x in enumerate(b.get("instructions", [])) if not x.get("note")]
    empty += [f"registers.{r['name']}.usage" for r in d.get("registers", []) if not r.get("usage")]
    if empty: W(f"todo: {len(empty)} empty prose fields, e.g. {', '.join(empty[:4])}")
    return report(errs, warns)


def entry_live_in(blocks, eu):
    ins_ = {b["id"]: set() for b in blocks}; changed = True
    while changed:
        changed = False
        for b in reversed(blocks):
            live = set()
            for s in b.get("successors", []):
                live |= ins_.get(s.get("target"), set()) | eu.get((b["id"], s.get("target")), set())
            for x in reversed(b.get("instructions", [])):
                live -= set(x.get("defs", [])) | set(x.get("clobbers", []) or [])
                live |= set(x.get("uses", []))
            if live != ins_[b["id"]]: ins_[b["id"]] = live; changed = True
    return ins_[blocks[0]["id"]] if blocks else set()


def report(errs, warns):
    for e in errs: print("ERROR", e)
    for w in warns: print("warn ", w)
    print(f"{len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
