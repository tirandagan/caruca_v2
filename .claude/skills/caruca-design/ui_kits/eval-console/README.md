# Eval Console UI kit
Recreation of caruca_v2's planned Web GUI (deferred/stretch component), built strictly from its spec in `ai_docs/prep/component_functionality.md` + `memory/component_functionality_spec.md`:
- side-by-side PTY terminal panes, **left = v1, right = v2**, xterm-style, over websocket
- a metrics panel reading the telemetry JSON the CLIs already write (tokens, cost, wall-clock, model-ID, seed)
- spawns existing `caruca-v2` subcommands; presentation layer only

Screens: Runs (telemetry run list + new-run form), Live comparison (dual terminals), Report (three-way comparison + percent-change roll-up). All data is representative fake data shaped by the spec's evaluation dimensions. No screenshots of a real GUI exist — this is a spec-faithful projection using the brand foundations, flagged as such.