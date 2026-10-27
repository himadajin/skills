#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Embed a JSON file into the template: python3 build.py data.json out.html
- Back-edges are (re)computed with the dominator rule (cfgtools.relabel_back_edges); the written
  branch kind is kept in 'cond_kind'.
- 'aliases' (text token -> canonical register, e.g. w8 -> x8) is added so the ISA-agnostic template
  can highlight sub-register spellings."""
import json, sys, re, pathlib
here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from cfgtools import relabel_back_edges
from validate import ISA, detect_isa
src = (here.parent / "assets" / "template.src.html").read_text(encoding="utf-8")
if len(sys.argv) != 3: sys.exit("usage: build.py data.json out.html")
data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
relabel_back_edges(data)
isa = detect_isa((data.get("function") or {}).get("isa"), "")
names = {r.get("name") for r in data.get("registers", [])}
al = {}
for b in data.get("blocks", []):
    for x in b.get("instructions", []):
        for t in re.findall(r"[A-Za-z][\w]*", x.get("text", "")):
            c = ISA[isa]["alias"].get(t.lower())
            if c and c in names and t not in names: al[t] = c
for p in (data.get("function") or {}).get("params", []):
    c = ISA[isa]["alias"].get(str(p.get("location", "")).lower())
    if c and c in names: al[p["location"]] = c
if al: data["aliases"] = al
blob = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
pathlib.Path(sys.argv[2]).write_text(src.replace("/*__DATA__*/", blob), encoding="utf-8")
