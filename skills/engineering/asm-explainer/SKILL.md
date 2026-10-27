---
name: asm-explainer
description: Turn one function of RISC-V or AArch64 assembly, or LLVM IR, into a readable single-file HTML explainer (control-flow graph, register roles, live ranges, per-block and per-instruction explanations, C source mapping) for the user's own study. Use when the user asks to explain, annotate, visualise or "read through" assembly / disassembly / LLVM IR / compiler output, asks "what does this asm do", "explain this RISC-V/AArch64 code", "make a CFG / register map / live ranges for this function", or gives C and wants to see what the compiler generates for it.
---

# asm-explainer

You read the listing and write a JSON file (references/schema.md); `scripts/validate.py` checks it against the listing; `scripts/build.py` renders one self-contained HTML file. No per-ISA analysis tool exists: the data comes from you, the validator is the safety net.

## Workflow
1. Get the input: one function's `.s` or `.ll`. If the user gives C, compile it yourself (`clang --target=riscv64-linux-gnu -march=rv64gc -S -O1 -g`, `clang --target=aarch64-linux-gnu -S -O1 -g`, `clang -S -emit-llvm -O1 -g0 -fno-discard-value-names`) — *`-g` gives `.loc` lines for the C mapping; -O1 keeps code short but realistic.*
2. Write the JSON exactly per [references/schema.md](references/schema.md) alone (its 'Minimal examples' section already has per-ISA snippets); do not look for or read example files — *the schema rules (block split, successors, defs/uses, roles) are what the validator enforces.*
3. `python3 scripts/validate.py data.json input.s --isa riscv|aarch64|llvm [--source foo.c]` and fix every ERROR, repeat until none — *its messages name the instruction and the expected value.*
4. Fill the prose fields (`function.summary`, block `summary`/`explanation`, instruction `note`, register `usage`, `notes`) in the user's language; in Japanese keep technical terms in English (taken / not taken, live range, control flow, basic block, back-edge, phi) — *readers match them against the graph labels.*
5. `python3 scripts/build.py data.json out.html` (or `uv run scripts/build.py …`) — *stdlib only, one HTML file, no network.*
6. Give the user the path of the HTML (open it if you can) and mention anything the validator only warned about.

## Rules
- Never invent defs/uses/successors: derive each from the operands in the listing — *the page's liveness is computed from them.*
- Treat validator ERRORs as right; only the cases listed under "Known limits" in references/testing.md may be false positives — *it has caught 68/68 injected mistakes.*
- Read every warn; fix it or say in `notes` why it is fine (e.g. a void callee you could not mark) — *warnings are heuristics, not noise.*
- Show every instruction of the function, verbatim; never summarise or drop lines — *the validator diffs the listing, and readers map the page back to it.*
- Roles, `source_line` and prose are descriptive aids, not guarantees; say so if the user relies on them — *they are checked only for consistency.*
- Do not restyle or edit `assets/template.src.html` — *the visual style is part of the tool.*
- For very large functions (> ~300 instructions) split by region or by function into several pages and tell the user — *the CFG and live-range table stop being readable.*
- One function per JSON — *block ids, roles and liveness are per function.*

## Files
- `scripts/validate.py`, `scripts/build.py`, `scripts/cfgtools.py` (Python ≥ 3.9, stdlib only); `assets/template.src.html`.
- [references/schema.md](references/schema.md): the JSON format and all rules (ABI/register naming included).
- [references/testing.md](references/testing.md): how the validator was tested and its known limits.
