"""caruca_v2 — LLM replication of caruca v1's specification-mining pipeline.

Every stage is a typed function under `stages/`; `cli.py` is a thin argparse wrapper
over those functions so an agent can call them directly.
"""

__version__ = "0.1.0"
