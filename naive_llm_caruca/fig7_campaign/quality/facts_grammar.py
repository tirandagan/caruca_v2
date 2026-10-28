#!/usr/bin/env python3
"""Load one syntax file through v1's own DSL and describe it for the program-checked facts.

For every node: its layout (syntax), position, type, spellings, `=` marker, repeat setting (arity),
sample values, and the forms v1's generator writes for it (max-arity 1, simple relations). Adapted
from naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/scripts/{normalize,render}.py.

    ~/dev/stevens/caruca/caruca/.venv/bin/python -I facts_grammar.py CMD SYNTAX_FILE > grammar.json
"""
import importlib.util, json, sys
from pathlib import Path

V1_SRC = Path.home() / "dev/stevens/caruca/caruca/src"
sys.path.insert(0, str(V1_SRC))
import caruca.ir.syntax as S  # noqa: E402

S.Argument.max_repetition = 1
S.Argument.elaborate_relations = False

cmd, path = sys.argv[1], sys.argv[2]
spec_mod = importlib.util.spec_from_file_location("t018_facts_spec", path)
mod = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(mod)
spec = getattr(mod, f"{cmd}_syntax_spec")

nodes = []
for si, syntax in enumerate(spec):
    for pi, pos in enumerate(syntax):
        for n in pos:
            rec = {"syntax": si, "position": pi, "type": type(n).__name__, "flag": n.flag,
                   "alias": list(getattr(n, "alias", []) or []),
                   "equals": bool(getattr(n, "flag_followed_by_equals", False)),
                   "arity": n.arity.name if hasattr(n.arity, "name") else str(n.arity),
                   "takes_value": not isinstance(n, S.Flag),
                   "dash_as_stdin": bool(getattr(n, "dash_as_stdin", False))}
            if n.flag:
                S.Path._counter = 1
                try:
                    rec["forms"] = [str(seq) for seq in n.syntax_variation() if seq.args]
                except Exception as exc:  # a node v1 cannot render is recorded, not hidden
                    rec["forms"], rec["render_error"] = [], f"{type(exc).__name__}: {exc}"
            nodes.append(rec)
json.dump({"command": cmd, "file": path, "n_syntaxes": len(spec), "nodes": nodes}, sys.stdout, indent=1)
