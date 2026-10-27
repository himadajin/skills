# asm-explainer JSON schema

You (an LLM) read one function of assembly (RISC-V, AArch64) or LLVM IR and write this JSON.
`python3 scripts/validate.py data.json input [--isa riscv|aarch64|llvm]` checks it (fix every ERROR, read every warn);
`python3 scripts/build.py data.json out.html` renders it. The template never parses assembly; it only uses these fields.
Prose fields (`summary`, `explanation`, `note`, `usage`, `notes`) are Japanese; may be `""` while drafting (shown as 未記入).

```
{
  "_comment": string?,                       // shown in footer
  "function": { "name", "isa", "summary", "compiler"?: string,
                "params":  [{ "name", "type", "location" }],   // location = register as written (w3) or %value
                "returns": { "type", "location" }? },          // omit for void
  "registers_title": string?,                // "Registers" (asm) | "SSA values" (LLVM)
  "blocks": [{
    "id": string,                            // unique; any stable string (bb0.. or the IR label)
    "label": string|null,                    // label as written, without ':' (LLVM also without '%': "4", "for.body"); null for unlabelled blocks
    "summary": string, "explanation": string,
    "instructions": [{ "text", "defs":[reg], "uses":[reg], "clobbers"?:[reg], "note"?, "source_line"?,
                       "callee_returns"?: "void"|"value" }],   // calls only; "void" = callee returns nothing
    "successors": [{ "target": block id, "kind": "true|false|jump|fallthrough|case|default",
                     "case"?: string | [string] }],      // only on kind "case": the case value(s), merged when several go to one target
    "jump_table"?: { "label": string, "targets": [block id] }   // asm indirect jump through a table: one entry per table slot, in order
  }],
  "registers": [{ "name", "role", "usage", "first_def"?, "last_use"? }],
  "edge_uses": [{ "from", "to", "uses":[reg] }]?,   // LLVM phi operands
  "notes": [string]?, "phi_note": string?,
  "source": { "language", "text" }?          // source_line is 1-based into this text
}
```

## Rules (each with the reason)

**Blocks**
- B1. `blocks` in listing (address) order; the first block is the entry. *Instruction numbering and fall-through depend on it.*
- B2. Every instruction of the function appears exactly once, `text` verbatim (whitespace may differ). *The validator diffs against the input.*
- B3. A block ends at its first branch / jump / return. A conditional branch followed by `j`/`b` therefore makes the `j` its own (unlabelled) block. A new label always starts a block. *One terminator per block keeps successors unambiguous.*
- B3a. Only labels that something branches to (a branch operand or a jump-table entry) start a block. Assembler-internal labels such as `.Lpcrel_hi0:` (target of `%pcrel_lo`), `.Ltmp3:`, `.Lfunc_begin0:` do **not** start a block and are not used as `label`. *They mark addresses for relocations/debug info, not control flow.*
- B3b. LLVM: the unnamed entry block has `label: null`; its implicit name is `%N` where N = number of (unnamed) parameters (`define i64 @f(i64 %0, i64 %1)` → entry is `%2`). Give it any id (recommended: the number, `"2"`); `edge_uses.from` and phi operands `[ %0, %2 ]` refer to it by that id. Multi-line instructions (`switch … [` … `]`) are one instruction; `text` is the joined line (`switch i32 %0, label %17 [ i32 0, label %4 i32 1, label %6 ]`).
- B4. LLVM: drop metadata attachments (`, !tbaa !6`, `, !llvm.loop !10`, `, !dbg !N`) from `text`; keep everything else (`#2`, `align 4`). *They carry no data flow and make lines long.*

**Successors** (write what the terminator says; the validator derives the same list)
- S1. Conditional branch: `true` = the branch target (taken), `false` = the next block in listing order (asm) or the second label (LLVM `br i1 %c, label %T, label %F` → T true, F false).
- S2. Unconditional jump (`j`, `b`, LLVM `br label %X`) → one `jump`. Even if X is the next block.
- S3. No terminator → one `fallthrough` to the next block. Return / tail call → no successors.
- S3a. Switch / jump table. LLVM `switch`: one `default` edge to the default label plus one `case` edge per distinct case target with `case` = the value(s) as strings (`"case": ["1","3"]` when two values share a target). asm jump table (`jr a0` / `br x10` through `.LJTI0_0`): set `jump_table: {label, targets}` with one block id per table entry in table order (duplicates kept), and one `case` edge per distinct target; `case` values are optional in asm (the index→value offset is usually computed by earlier code). The range check before it (`bltu a3, a0, .LBB0_8`, `b.hi`) stays an ordinary `true`/`false` branch; asm never uses `default`. The validator reads the table directives (`.word/.long/.quad/.byte …`) from the input and requires the same targets.
- S4. Do **not** write `back`. `build.py` marks an edge `back` when its target dominates its source (natural-loop back-edge) and keeps your kind as `cond_kind`; a taken branch that is also a back-edge is still written `true`. *Loop detection is mechanical; the LLM should only transcribe branches.* (`back` is still accepted with a warning, and rejected on an edge that is not a back-edge.)

**Register names** (asm)
- N1. In `defs`/`uses`/`clobbers`/`registers` use the canonical full-width name; `text` keeps what was written.
  AArch64: `w8`→`x8`, `wzr`→(omitted), `wsp`→`sp`, `lr`→`x30`, `fp`→`x29`, `b/h/s/d/q/vN`→`vN`, flags = `nzcv`.
  RISC-V: ABI names (`x10`→`a0`, `fp`→`s0`, `f10`→`fa0`). *w8 and x8 are one register; split names break liveness.*
- N2. Zero registers (`xzr`, `wzr`, `zero`/`x0` on RISC-V) never appear in defs/uses. *Reading them carries no value.*
- N3. LLVM: names are the `%values` (`%0`, `%add`); parameters included; constants, labels and `@globals` are not values.

**defs / uses** — per operand position, not just "mentioned somewhere"
- D0. Immediates, relocations (`%lo(sym)`, `:lo12:sym`) and shift/extend keywords are never registers (`tst x0, #0x1` uses only x0).
- D1. Default: first register operand is written, the rest are read (`add x8, x9, x8`: defs [x8], uses [x9, x8]).
- D2. Stores read every register operand (`sd ra, 40(sp)`, `str w18, [x16, x14, lsl #2]`, `stp x29, x30, [sp, #16]`). Compares (`cmp`, `cmn`, `tst`, `fcmp`) write only flags. Conditional compares (`ccmp`, `ccmn`, `fccmp`) read their register operands and `nzcv`, and write only `nzcv` (`ccmp x8, #0, #4, le`: defs [nzcv], uses [x8, nzcv]). Branches (`beq`, `cbz`, `tbz`) only read.
- D3. Load pair (`ldp a, b, [...]`) writes both a and b.
- D4. Pre/post-index writeback (`[x7], #4`, `[sp, #-16]!`) also **writes the base** (defs gets x7 / sp).
- D5. Read-modify-write: destination is also read for `movk`, `bfi`, `bfxil`, `mla`/`fmla` (vector), `ins`, RISC-V `c.add`-style 2-operand forms. (`madd d, n, m, a` is not RMW: a is an ordinary source.)
- D6. Hidden operands. AArch64: `cmp/cmn/tst/subs/adds/ands/bics/negs/ccmp` write `nzcv`; `b.cond/csel/csinc/csinv/csneg/cset/cinc/cneg/adc/sbc/ccmp` read `nzcv`. `ret` reads `x30` (RISC-V `ra`) plus the return register unless void: `x0`/`a0` for integers and pointers, `v0`/`fa0` for floating point (written `d0`/`s0` in AArch64 text, canonical `v0`). Calls (`bl`, `blr`, `call`, `jal`) write `x30`/`ra` and the return register `x0`/`a0` (unless the callee is void), and read the argument registers set up for them (x0–x7, v0–v7 / a0–a7, fa0–fa7 written since the previous call). The validator gives an ERROR when an argument register was written in the same block since the last call and not read before the call (such a write is dead unless the callee reads it, because the call clobbers it); if it was also read in between it only warns. No flags on RISC-V.
- D6a. Void callees: a call to a function returning `void` does not def `x0`/`a0` (it goes in `clobbers`); mark the instruction `"callee_returns": "void"` so the validator knows. `validate.py … --source foo.c` (or a `.ll` input) lets it infer `void` from the prototype.
- D7. Calls should list `clobbers`: the caller-saved registers they destroy that are not in defs. RISC-V: a0–a7, t0–t6, fa0–fa7, ft0–ft11. AArch64: x0–x17, v0–v7, v16–v31, nzcv. Optional (warn if missing): *without them liveness runs straight through the call.* Callee-saved registers must not be listed.
- D8. LLVM: `%x = ...` defs [%x]; uses = every `%value` operand (both operands of `store`, all `getelementptr` operands, call arguments). `store`, `br`, `ret void` define nothing.
- D9. LLVM phi: `uses` is `[]`; each `[ %v, %pred ]` goes into `edge_uses` as `{from: pred block, to: phi block, uses:[%v]}` (constants omitted; `undef`, `poison`, `null`, `zeroinitializer` count as constants). *A phi operand is read at the end of the predecessor, on that edge only.*

**Roles** (`role` = role in this function)
| value | use for |
|---|---|
| `argument` / `argument+return` | holds a parameter on entry (even if later reused as scratch — say so in `usage`); LLVM parameters |
| `return` | carries the return value only (LLVM: the value given to `ret`) |
| `callee-saved` | saved/restored callee-saved register (x19–x28, s0–s11), even if used as a temporary |
| `temporary` | written before read, caller-saved scratch |
| `return-address` (`ra`/`x30`), `stack-pointer` (`sp`), `frame-pointer` (`x29` as FP), `flags` (`nzcv`), `zero` | fixed |
| `ssa-value` | every other LLVM value |
| `undefined-live-in` | read before any write on some path, but not a parameter location and not callee-saved: the code reads an undefined value there (seen at -O1 where the value is never observable) |
| `other` | none of the above |
- R1. A register read before any write (live at entry) is never `temporary`. *It carries an incoming value.* A live-in callee-saved register marked `temporary` is an ERROR.
- R2. A register that holds a parameter on entry and is also the return register read by `ret` is `argument+return` (not `argument`, not `return`).
- R3. `x29` (RISC-V `s0`) set from `sp` in the prologue (`mov x29, sp`, `add x29, sp, #16`, `addi s0, sp, 32`) is `frame-pointer`, not `callee-saved`.
- R4. LLVM: a value given to `ret` is `return`, even if it is also a phi / loop value (`%4 = phi …` returned by `ret i64 %4`). A parameter given to `ret` is `argument+return`.

**source_line**
- L1. asm: the line of the latest `.loc` before the instruction, **not carried across a branch-target label** (`.LBB0_3:`, gcc `.L3:`): after such a label, instructions before the next `.loc` have no line. Omit when the line is 0 or there is none. Unlabelled fall-through blocks (`# %bb.1:`) do carry it (same straight-line code). LLVM without `!dbg`: omit. *A label joins paths; the previous block's line would be wrong for the other path.*

## Minimal examples (prose omitted)
RISC-V
```
{"text":"ld\ta3, 0(a0)","defs":["a3"],"uses":["a0"],"source_line":4}
{"text":"call\thelper","defs":["ra","a0"],"uses":["a0"],"clobbers":["a1","a2","a3","a4","a5","a6","a7","t0","t1","t2","t3","t4","t5","t6","fa0","fa1","fa2","fa3","fa4","fa5","fa6","fa7","ft0","ft1","ft2","ft3","ft4","ft5","ft6","ft7","ft8","ft9","ft10","ft11"]}
{"text":"bne\ta0, a1, .LBB0_2","defs":[],"uses":["a0","a1"]}   successors: [{"target":"bb2","kind":"true"},{"target":"bb3","kind":"false"}]
{"text":"ret","defs":[],"uses":["ra","a0"]}
```
AArch64
```
{"text":"stp\tx29, x30, [sp, #-48]!","defs":["sp"],"uses":["x29","x30","sp"]}
{"text":"ldr\tw19, [x7], #4","defs":["x19","x7"],"uses":["x7"]}
{"text":"cmp\tw5, #1","defs":["nzcv"],"uses":["x5"]}
{"text":"b.lt\t.LBB0_2","defs":[],"uses":["nzcv"]}
{"text":"mov\tw8, wzr","defs":["x8"],"uses":[]}
{"text":"ret","defs":[],"uses":["x30","x0"]}
```
Jump table (RISC-V; AArch64 `br x10` is the same)
```
{"text":"jr	a0","defs":[],"uses":["a0"]}
"jump_table": {"label":".LJTI0_0","targets":["bb2","bb6","bb4","bb5","bb3","bb7"]},
"successors": [{"target":"bb2","kind":"case","case":"0"},{"target":"bb6","kind":"case","case":"1"}, …]
```
LLVM IR
```
{"text":"%i = phi i64 [ 0, %entry ], [ %inc, %loop ]","defs":["%i"],"uses":[]}   edge_uses: [{"from":"loop","to":"loop","uses":["%inc"]}]
{"text":"%p = getelementptr inbounds i32, ptr %a, i64 %i","defs":["%p"],"uses":["%a","%i"]}
{"text":"store i32 %v, ptr %p, align 4","defs":[],"uses":["%v","%p"]}
{"text":"br i1 %c, label %exit, label %loop","defs":[],"uses":["%c"]}   successors: [{"target":"exit","kind":"true"},{"target":"loop","kind":"false"}]
{"text":"switch i32 %0, label %17 [ i32 0, label %4 i32 1, label %6 i32 2, label %4 ]","defs":[],"uses":["%0"]}
   successors: [{"target":"17","kind":"default"},{"target":"4","kind":"case","case":["0","2"]},{"target":"6","kind":"case","case":"1"}]
```

## Rendering notes
- Liveness is computed in the browser (backward dataflow; `clobbers` kill, `edge_uses` are live-out of `from`).
- CFG: `case` edges are labelled with their value(s), `default` is drawn dash-dot and labelled `default`. A fan-out of more than 4 targets in one layer is wrapped into two staggered rows when the graph is wider than the page; if it is still wider, the CFG scrolls sideways with a fade on the clipped side and a `← scroll →` hint.
- CFG: layered layout (back-edges excluded from layering). Within a layer, blocks are ordered by their predecessors' positions (fewer crossings), ties by listing order; each node shows its listing index `#n` at the top right so `.LBB0_5`/`.LBB0_6` can be mapped to the listing. Lines wider than ~440px are truncated with `…` (full text in the tooltip and in the listing).
- `build.py` adds `aliases` (e.g. `w8`→`x8`) so written sub-register names highlight with their canonical register.
- The detail panel is stacked below the CFG when the graph is wider than 58% of the content (always under 960px).
