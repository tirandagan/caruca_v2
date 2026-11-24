---
name: feedback-pash-runs-test-our-annotations
description: When Tiran asks to run PaSh benchmark suites, the point is to test our annotation files (naive LLM's, or Caruca's) against PaSh's own; a run with only PaSh's stock annotations is useless to him
metadata:
  type: feedback
---
A PaSh benchmark run is only useful to Tiran when it runs **our** annotation files: the naive LLM's PaSh
files (and/or Caruca's), compared with PaSh's original annotations, with outputs checked against bash.

**Why:** on 2026-11-24 he called the 2026-11-22/23 Koala run "useless" because it used only PaSh's stock
annotations, and had its results deleted. His request had been "run all the osdi22 test scripts"; the
annotation set was never stated, and the run went ahead without asking.

**How to apply:** before any PaSh run, state which annotation sets will be loaded (stock, naive LLM's,
Caruca's) and confirm the comparison if the request doesn't say. Load a set with PaSh's
`--local-annotations-dir` on a private copy of the package (task 022's `run_pash.py`, `build_set`), never by
editing the installed package. Results of naive-LLM PaSh runs go under `naive_llm_caruca/runs/`.
Related: [[reference-pash-annotations-runtime]], [[reference-pash-comparison-scorer]].
