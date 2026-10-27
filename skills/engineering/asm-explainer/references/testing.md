# How the validator was tested

- **Mutation test**: 68 known mistakes injected into correct JSONs (wrong/missing defs and uses, hidden operands such as nzcv / x30 / writeback, successor kinds and targets, jump-table and `switch` edges, edge_uses, roles, call arguments, void callees, `source_line`); all 68 are reported (61 as ERROR, 7 as warn for heuristic checks). The corpus is not shipped (it is ~1 MB of listings).
- **Three clean-room rounds**: an LLM wrote JSON from schema.md alone for 9 + 16 + 18 functions (sum/process/matmul; strlen, float dot product, switch/jump tables, recursion, 128-bit/popcount/csel; bsearch, memcpy, collatz, list walk, clamp, saturating add) × RISC-V / AArch64 / LLVM. Each round's validator false positives and gaps were fixed; all 43 JSONs now validate with 0 errors.
- **Independent audit** (round 3, 364 instructions re-derived by hand): 0 data errors found. With that sample size the residual error rate is bounded only to roughly **2–3 per 100 instructions** per ISA (95 %).

## Known limits
- No test coverage for SIMD/vector code beyond a few scalar-FP and `cnt` cases, atomics/exclusives, `indirectbr`/`invoke`/`callbr` (successors not checked: warn), exceptions, gcc output beyond a couple of files, x86.
- Call arguments: only setups in the same block as the call are checked; an argument register read before the call is only a warning. Whether a callee returns void is known only from `callee_returns` or `--source`.
- Case values of assembly jump tables are not checked (only the targets and their order).
- Roles are checked for live-in / return / frame-pointer consistency only; `usage` text and prose are never checked.
