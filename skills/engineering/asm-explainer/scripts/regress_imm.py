#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Regression: immediates / relocations / shift keywords are never read as registers (validate.expected_asm)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import expected_asm, ISA
CASES = [  # (isa, text, defs, uses)
 ("aarch64", "tst x0, #0x1", ["nzcv"], ["x0"]),
 ("aarch64", "add x0, x1, #0x10", ["x0"], ["x1"]),
 ("aarch64", "ldr x0, [x1, #16]", ["x0"], ["x1"]),
 ("aarch64", "mov w0, #1", ["x0"], []),
 ("aarch64", "add x9, x9, :lo12:.LJTI0_0", ["x9"], ["x9"]),
 ("aarch64", "add x10, x10, x11, lsl #2", ["x10"], ["x10", "x11"]),
 ("aarch64", "ldr w8, [x9, w10, uxtw #2]", ["x8"], ["x9", "x10"]),
 ("aarch64", "and w9, w1, #0xff", ["x9"], ["x1"]),
 ("aarch64", "movi d1, #0000000000000000", ["v1"], []),
 ("aarch64", "fmov d0, #1.00000000", ["v0"], []),
 ("riscv", "li a0, 0x10", ["a0"], []),
 ("riscv", "li a0, 0x1", ["a0"], []),
 ("riscv", "addi a0, a1, %lo(sym)", ["a0"], ["a1"]),
 ("riscv", "lui a0, %hi(x1)", ["a0"], []),
 ("riscv", "auipc a3, %pcrel_hi(.LJTI0_0)", ["a3"], []),
 ("riscv", "addi a3, a3, %pcrel_lo(.Lpcrel_hi0)", ["a3"], ["a3"]),
 ("riscv", "lw a0, 0(a0)", ["a0"], ["a0"]),
 ("riscv", "sd ra, 24(sp)", [], ["ra", "sp"]),
]
bad = 0
for isa, t, d, u in CASES:
    D, U = expected_asm(t, isa, ISA[isa], None)[:2]
    if D != d or U != u: bad += 1; print(f"FAIL {isa:8} {t!r}: got defs {D} uses {U}, want {d} {u}")
print(f"{len(CASES) - bad}/{len(CASES)} immediate-parsing cases pass"); sys.exit(1 if bad else 0)
