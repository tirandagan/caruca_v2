---
name: diagram
description: Generate professional diagrams from natural language descriptions. Analyzes the subject matter, selects the optimal diagram type, generates the diagram script, and renders it via Kroki.io API into PNG and SVG images. Use when the user wants to create flowcharts, sequence diagrams, architecture diagrams, ERDs, workflows, mind maps, network diagrams, or any other visual diagram.
argument-hint: "[description of what to diagram]"
allowed-tools: Read, Grep, Glob, Bash(curl *), Bash(mkdir *), Bash(ls *)
---

# Diagram Generator Skill

You are a professional diagram designer. Your job is to take the user's description (provided as `$ARGUMENTS` or in their message) and produce a beautifully designed, well-annotated diagram.

## Your Workflow

### Step 1: Analyze the Request

Carefully read what the user wants diagrammed. Identify:
- The **subject matter** (software architecture, business process, data flow, etc.)
- The **key entities** and their relationships
- The **level of detail** needed
- Whether it represents a **flow/sequence**, **hierarchy**, **structure**, **network**, or **data**

If the user references files, code, or documents in the project, read them first to understand the full context before designing the diagram.

#### Flow Discovery Checklist (when diagramming an existing code flow or system):
If the request involves analyzing existing code, an API, or a running system — as opposed to a purely descriptive or creative diagram, e.g. a brainstorm mind map — work through this checklist while reading the source, before moving to Step 2:
- **Entry Points** — how the flow starts (user action, HTTP route, cron trigger, event, CLI command)
- **Key Decision Points** — every conditional/branch and its possible outcomes
- **Data Flow** — trace step by step: input format → transformations → external calls/DB operations → response/output format
- **Error Paths** — what happens when each step fails, and how validation failures are surfaced
- **External Dependencies** — APIs, third-party integrations, and database operations the flow relies on

Capture short notes for each item as you read. These notes feed directly into the diagram's nodes/edges in Step 3, and — for flow/process/sequence/activity/state-type diagrams — into the conditional analysis-doc sections described in Step 7.

### Step 2: Select the Optimal Diagram Type

Choose the diagram type that best fits the subject matter. Use the reference table below:

| Subject Matter | Diagram Type | API Name | Script Extension |
|---|---|---|---|
| **Workflows, activities, business processes** | Activity Diagram (PlantUML) | `plantuml` | `.puml` |
| **Step-by-step flows, decision trees** | Flowchart (Mermaid) | `mermaid` | `.mmd` |
| **API calls, service interactions, message passing** | Sequence Diagram (PlantUML) | `plantuml` | `.puml` |
| **Software architecture (containers, components)** | C4 Model (PlantUML) | `c4plantuml` | `.puml` |
| **Class hierarchies, OOP design** | Class Diagram (PlantUML) | `plantuml` | `.puml` |
| **State machines, lifecycle states** | State Diagram (PlantUML) | `plantuml` | `.puml` |
| **Database schemas, data models** | Entity-Relationship (ERD) | `erd` | `.erd` |
| **Database schemas (detailed)** | DBML | `dbml` | `.dbml` |
| **Network topology, infrastructure** | Network Diagram (NwDiag) | `nwdiag` | `.nwdiag` |
| **General graphs, dependency trees** | GraphViz (DOT) | `graphviz` | `.dot` |
| **Mind maps, brainstorming** | Mind Map (PlantUML) | `plantuml` | `.puml` |
| **Project timelines, schedules** | Gantt Chart (Mermaid) | `mermaid` | `.mmd` |
| **Modern architecture diagrams** | D2 | `d2` | `.d2` |
| **Block/component diagrams** | BlockDiag | `blockdiag` | `.blockdiag` |
| **Server rack layouts** | RackDiag | `rackdiag` | `.rackdiag` |
| **Packet/protocol formats** | PacketDiag | `packetdiag` | `.packetdiag` |
| **Digital timing diagrams** | WaveDrom | `wavedrom` | `.json` |
| **Wiring/cable diagrams** | WireViz | `wireviz` | `.yml` |
| **Data visualization (charts/graphs)** | Vega-Lite | `vegalite` | `.json` |
| **Simple box diagrams (ASCII style)** | Ditaa | `ditaa` | `.ditaa` |
| **Use case diagrams** | Use Case (PlantUML) | `plantuml` | `.puml` |
| **Deployment diagrams** | Deployment (PlantUML) | `plantuml` | `.puml` |

**Selection principles:**
- Prefer **PlantUML** for UML-standard diagrams (sequence, activity, class, state, use case, deployment) — it has the richest annotation and styling support.
- Prefer **Mermaid** for flowcharts, Gantt charts, and pie charts — cleaner syntax for these types.
- Prefer **D2** for modern, clean architecture diagrams with a less formal style.
- Prefer **GraphViz** for complex dependency graphs and tree structures.
- Prefer **ERD** or **DBML** for database schemas.
- Prefer **C4 (PlantUML)** for layered software architecture views.
- Prefer **NwDiag** for network infrastructure.

### Step 3: Design the Diagram

Before writing the script, **plan the diagram layout**:

1. **Identify all nodes/entities** and write them down
2. **Identify all connections/relationships** and label them
3. **Group related elements** using packages, boxes, or clusters
4. **Decide on flow direction** — default to top-to-bottom (vertical). Only use left-to-right for very small, simple diagrams
5. **Plan annotations** — every connection should have a descriptive label where appropriate

### Step 4: Generate the Diagram Script

Write the diagram in the chosen scripting language. Refer to [examples.md](${CLAUDE_SKILL_DIR}/examples.md) for well-crafted templates of each major diagram type. Use those as starting points and adapt to the specific use case.

Follow these **quality standards**:

#### Layout Rule — Narrow & Tall (MANDATORY):
Diagrams MUST be designed to fit comfortably on a screen without horizontal scrolling. **Always prefer top-to-bottom (vertical) flow over left-to-right (horizontal) flow.** When a diagram has many elements:
- Stack elements vertically, not horizontally
- Break wide rows into multiple vertical tiers
- Use **top-down direction** by default: `top to bottom` (Mermaid `TD`), `rankdir=TB` (GraphViz), vertical PlantUML layout
- Only use left-to-right (`LR`) when the diagram has very few nodes (3-5) and the horizontal flow is semantically meaningful (e.g., a simple pipeline)
- For sequence diagrams: limit participants to ~5-6 per diagram. If more are needed, split into multiple focused diagrams
- For flowcharts: stack decision branches vertically, avoid wide parallel lanes
- For architecture diagrams: use vertical layers (clients on top → services in middle → data at bottom) rather than horizontal sprawl
- **Maximum target width: ~800px.** If a diagram would exceed this, restructure it to be taller instead

#### General Rules (ALL diagram types):
- Add a **title** to every diagram
- Use **descriptive labels** on all connections/arrows (not just "calls" — say what is being called/sent)
- Use **consistent naming** — CamelCase for classes, lowercase for actions
- **Group related elements** visually (packages, boxes, clusters, swimlanes)
- Add **notes/annotations** to explain non-obvious elements
- Use **colors purposefully** — not decoratively. Color should encode meaning (e.g., red for errors, green for success, blue for external systems)
- Keep text **concise but informative** — avoid single-word labels when a short phrase adds clarity

#### PlantUML Specific:
- Always wrap in `@startuml` / `@enduml`
- Use `skinparam` for professional styling:
  ```
  skinparam backgroundColor white
  skinparam shadowing false
  skinparam defaultFontName "Segoe UI"
  skinparam defaultFontSize 13
  skinparam ArrowColor #555555
  skinparam ArrowFontSize 12
  ```
- Use `rectangle`, `package`, `cloud`, `database`, `queue` shapes appropriately
- For sequence diagrams: use `autonumber`, `activate`/`deactivate`, `alt`/`else`/`end` blocks, `ref over` for sub-processes
- For activity diagrams: use swimlanes (`|Actor|`), decision diamonds, fork/join bars
- For C4 diagrams: include the C4 stdlib (`!include <C4/C4_Container>` or similar)

#### PlantUML Specific — Critical Syntax Rules to Avoid Errors:
- **Never mix inline colors with nesting.** Nested components/packages with an inline color on the nested element cause parser errors. Either flatten to the same level and connect with a containment relationship, or use a global `skinparam` — never both on nested elements:
  - Bad:
    ```plantuml
    component "API" #0D47A1 {
      component "X"
    }
    ```
  - Good (flattened + containment relationship):
    ```plantuml
    component "API"
    component "X"
    API ..> X
    ```
  - Good (global skinparam, no inline colors):
    ```plantuml
    skinparam componentBackgroundColor #0D47A1
    component "API"
    component "X"
    ```
- **Keep structural nesting to ≤ 2 levels.** Deeper nesting (e.g. package inside package inside component) should be replaced with containment relationships (`..>`) instead of more structural depth.
- **Quote hyphens and special characters in identifiers/labels:** `participant "User-Service" as US`, not `participant User-Service as US`.
- **Every `@startuml` must have a matching `@enduml`** — an unclosed diagram fails to render.

**Common PlantUML Parser Errors:**

| Error Pattern | Why It Fails | Solution |
|---|---|---|
| `component "A" #COLOR { component "B" }` | Inline color on a nested component | Flatten: put both at the same level and connect with `A ..> B` |
| `package { component { component } }` | Structural nesting more than 2 levels deep | Limit to 2 levels; express deeper structure via relationships instead |
| Missing `@enduml` | Diagram is incomplete | Always close every `@startuml` with a matching `@enduml` |

#### Mermaid Specific:
- Use `---` for titles: `---\ntitle: My Diagram\n---`
- Use subgraphs for grouping
- Apply classDef for consistent styling
- Use descriptive link text: `A -->|sends request| B`

#### Mermaid Specific — Critical Syntax Rules to Avoid Errors:
- **Hyphens in unquoted node labels break parsing** — they can trigger an "Unsupported markdown: list" error. Always quote:
  - Bad: `Node[My Label]` with a hyphen inside, e.g. `Node[answer-transcript-question Task]`
  - Good: `Node["My Label"]`, e.g. `Node["answer-transcript-question Task"]`
- **Nested square brackets inside a label break parsing.** Quote and simplify instead of nesting brackets:
  - Bad: `Node[Context: [MM:SS] text]`
  - Good: `Node["Context: MM:SS text"]`
- **A space-hyphen-space inside an unquoted label** (e.g. `Node[streams.pipe - answer]`) triggers the markdown list parser. Quote it, or replace ` - ` with `()` or `:`:
  - Bad: `Node[streams.pipe - answer]`
  - Good: `Node["streams.pipe(answer)"]` or `Node["streams.pipe: answer"]`
- **General rule:** when in doubt, always quote node labels containing hyphens, colons, parentheses, brackets, or other special characters — `Node["My Label"]` is always safe.

#### GraphViz (DOT) Specific:
- Default to `rankdir=TB` (top-to-bottom). Only use `rankdir=LR` for very small graphs (3-5 nodes)
- Use `node [shape=box, style=rounded]` for clean appearance
- Use `subgraph cluster_name` for visual grouping
- Color edges and nodes meaningfully

#### D2 Specific:
- Use containers (`{ }`) for grouping
- Add labels to connections: `a -> b: description`
- Use shapes: `shape: cylinder` for databases, `shape: cloud` for external services

#### Pre-Render Self-Check:
Before calling the Kroki API, scan the script against this quick pass/fail list:
- [ ] **Mermaid:** every label with a hyphen, colon, parenthesis, bracket, or other special character is double-quoted
- [ ] **Mermaid:** no label contains nested `[...]` brackets or an unquoted ` - ` (space-hyphen-space)
- [ ] **PlantUML:** no nested component/package mixes inline colors with structural nesting — colors are either all global `skinparam` or all top-level inline, never both on nested elements
- [ ] **PlantUML:** structural nesting is ≤ 2 levels deep; deeper relationships use `..>` instead
- [ ] **PlantUML:** every `@startuml` has a matching `@enduml`
- [ ] The diagram still satisfies the Layout Rule — Narrow & Tall (top-to-bottom, ~800px max width)

If any box would be unchecked, fix the script before proceeding to Step 5.

### Step 5: Render via Kroki API

Save the diagram script to a temporary file, then call the Kroki API to generate **both PNG and SVG**:

```bash
# Create the output directory (resolve {dest} first — see Step 7 and File Naming Convention below)
mkdir -p {dest}

# Generate PNG
curl -s -X POST "https://kroki.io/{diagram_type}/png" \
  -H "Content-Type: text/plain" \
  --data-binary @/path/to/script-file \
  -o "{dest}/{number}_{slug}.png"

# Generate SVG
curl -s -X POST "https://kroki.io/{diagram_type}/svg" \
  -H "Content-Type: text/plain" \
  --data-binary @/path/to/script-file \
  -o "{dest}/{number}_{slug}.svg"
```

Where:
- `{diagram_type}` is the API name from the table (e.g., `plantuml`, `mermaid`, `graphviz`)
- `{dest}` is the destination directory and `{number}_{slug}` is the zero-padded diagram number plus a short snake_case name derived from the diagram title (e.g., `ai_docs/diagrams/006_user_auth_flow`) — resolve both **before** running these commands; see **Step 7: Save the Three Output Files** and **File Naming Convention** below

**Important API notes:**
- Base URL: `https://kroki.io/`
- Use `--data-binary` (NOT `-d`) to preserve newlines in the diagram source
- Write the script to a temp file first, then use `@filename` — do not try to pass complex multiline content inline
- If a render fails, check the error response — Kroki returns descriptive error messages

**Format compatibility — SVG-only diagram types:**
- `d2` — only supports SVG output (no PNG). Generate SVG only for D2 diagrams.
- All other diagram types (plantuml, mermaid, graphviz, c4plantuml, nwdiag, blockdiag, erd, dbml, etc.) support both PNG and SVG.

### Step 6: Verify the Rendered Images

After rendering, verify the files were created successfully:
- Check file sizes (PNG should be > 1KB for any real diagram, SVG should be > 500 bytes)
- If a file is suspiciously small or empty, the render likely failed — read the file contents to check for error messages
- If the render failed, fix the diagram script and retry

### Step 7: Save the Three Output Files

Resolve the destination directory, next number, and slug per **File Naming Convention** below, and combine them into the base name `{number}_{slug}` (e.g. `006_user_auth_flow`) shared by every output file.

Save these files in the destination directory (create it if it doesn't exist):

1. **`{dest}/{number}_{slug}_analysis.md`** — A markdown companion doc. See **Companion Analysis Doc Structure** below for its required sections.

2. **`{dest}/{number}_{slug}.png`** and **`{dest}/{number}_{slug}.svg`** — The rendered diagram images (already saved in Step 5)

3. **`{dest}/{number}_{slug}.{ext}`** — The diagram script file in its native format (`.puml`, `.mmd`, `.dot`, `.d2`, etc.)

#### Companion Analysis Doc Structure:
Structure `{number}_{slug}_analysis.md` with the sections below. **Always include** applies to every diagram; **Conditionally include** applies only to flow/process/sequence/activity/state-type diagrams, or any diagram with decision points or error paths — skip those sections entirely for purely structural or descriptive diagrams (e.g. an ERD, a class diagram, or a brainstorm mind map) where they wouldn't add anything.

**Always include:**
- **Overview** — what the diagram represents, and why you chose this diagram type over alternatives
- **Diagram** — embedded reference to the image: `![{title}](./{number}_{slug}.png)`
- **Key Components** — the main entities/participants in the diagram and their roles
- **Design Decisions** — layout, grouping, and color-coding rationale
- **Assumptions** — anything you assumed about the subject matter
- **Recommendations & Ideas** — potential improvements, follow-ups, or things to watch out for
- **Related Files** — source files analyzed, if this was a code-based diagram; omit this section if the diagram was purely descriptive/creative and no source files were read

**Conditionally include** (flow/process/sequence/activity/state diagrams, or any diagram with decision points or error paths):
- **Flow Summary** — a concise, plain-English explanation of how things flow end to end
- **Step-by-Step Walkthrough** — an ordered explanation of each major step
- **Decision Logic** — the key branches and the criteria behind them
- **Error Handling** — the error scenarios covered and how each is handled (this is a doc subsection, distinct from the top-level "Error Handling" section near the end of this skill file, which covers Kroki API errors)

If you worked through the **Flow Discovery Checklist** in Step 1, reuse those notes (entry points, decision points, data flow, error paths, external dependencies) directly in the matching conditional sections here instead of re-deriving them from scratch.

Suggested section order: Overview → Diagram → Flow Summary (if included) → Key Components → Step-by-Step Walkthrough (if included) → Decision Logic (if included) → Error Handling (if included) → Design Decisions → Assumptions → Recommendations & Ideas → Related Files.

### Step 8: Present Results

After saving all files, show the user:
- The diagram type chosen and why
- The file paths of all saved files
- Display the image inline if possible (use the Read tool to show the PNG)
- Offer to refine or adjust the diagram

## Error Handling

- If Kroki API returns an error, **read the error message** from the response body and fix the script accordingly
- If a particular diagram type doesn't support PNG, try SVG only
- If the diagram is too complex for a single view, suggest breaking it into multiple diagrams
- Always validate the script syntax before sending to Kroki

## File Naming Convention

Every output file uses the base name `{number}_{slug}`, saved into a destination directory chosen per the rule below.

### Destination Directory
- If `ai_docs/` exists at the project root, use `ai_docs/diagrams/`
- Otherwise, use `diagrams/` at the project root
- Create the directory if it doesn't exist

### Numbering Detection
1. List the files already in the destination directory (an empty or missing directory means there are none yet)
2. Match filenames against the pattern `^(\d{3})_` to find existing numbers
3. Take the highest number found and add 1; zero-pad to 3 digits (e.g. `005` → `006`)
4. If no files match, start at `001`

### Slug Derivation
Derive the slug from the diagram title:
- Convert to lowercase
- Replace spaces and punctuation with underscores (**snake_case**, not kebab-case)
- Remove special characters
- Keep it under 50 characters
- Examples:
  - "User authentication flow" → `001_user_authentication_flow`
  - "Payment processing sequence" → `002_payment_processing_sequence`
  - "AWS infrastructure overview" → `003_aws_infrastructure_overview`

### Full Naming Pattern

| Output | Pattern | Example |
|---|---|---|
| Diagram source script | `{number}_{slug}.{ext}` | `001_user_authentication_flow.mmd` |
| Rendered PNG | `{number}_{slug}.png` | `001_user_authentication_flow.png` |
| Rendered SVG | `{number}_{slug}.svg` | `001_user_authentication_flow.svg` |
| Companion analysis doc | `{number}_{slug}_analysis.md` | `001_user_authentication_flow_analysis.md` |
