# Course Tools

Two real, data-backed tools for the Python design pattern course AI assistant:

1. **Course chapter lookup** - search the 28 Labs and their knowledge points.
2. **Knowledge point prerequisite / related relation lookup** - report recorded
   comparison, alternative, and candidate ordering relations.

Both tools read `data/chapters.json` and `data/prerequisites.json`. They never
invent chapters, knowledge points, or prerequisite edges, and they do not embed
answers in a prompt.

## Project Layout

```text
course-tools/
├── commands/                    # CLI entry points
├── data/
│   ├── chapters.json            # 28 Labs, knowledge points, sources
│   ├── prerequisites.json       # relations with evidence
│   └── schemas/                 # JSON Schema for the two data files
├── docs/
│   ├── tool-contract.md
│   └── open-webui-integration.md
├── openwebui/                   # Open WebUI Function wrappers
├── skills/
│   └── course_practice_generator/ # Course-grounded Open WebUI Skill
├── mcp/
│   └── course_quiz_grader/       # Deterministic MCP Streamable HTTP server
├── scripts/
│   └── validate_curriculum.py   # data validation script
├── src/course_tools/            # query implementation
└── tests/                       # unittest suite
```

The upstream knowledge base is not modified. `course-tools/` is independent and
reads the cloned repository at `../python-design-pattern-rag` only to verify that
referenced source files exist.

## Data Provenance

- The 28 learning units are ordered by `labs/index.md`.
- English titles are the original titles; Chinese titles are display aliases.
- `pattern_kind` is `gof`, `python_idiom`, or `architecture`.
- `confirmed_prerequisites` is empty because no file states a formal prerequisite.
- Explicit comparison/alternative/confusion relationships are in `related`.
- Candidate orderings that cannot be confirmed are in `unconfirmed`.
- Every chapter and knowledge point carries real source files and evidence.
- There are no question-bank fields such as `options`, `correct_answer`, or `score`.

## Command Line Usage

Requires Python 3.9 or newer. No third-party packages are needed.

Chapter lookup:

```powershell
python commands/course_chapter_lookup.py --query Observer --include-knowledge-points
python commands/course_chapter_lookup.py --category creational --limit 20
python commands/course_chapter_lookup.py --pattern-kind architecture
```

Prerequisite lookup:

```powershell
python commands/course_prerequisite_lookup.py "Factory Method"
python commands/course_prerequisite_lookup.py Singleton --direction all
python commands/course_prerequisite_lookup.py lab-07-state-kp-comparison
```

The commands return JSON and exit with status 0 on success or 1 when the query
is invalid.

## Validation

```powershell
python scripts/validate_curriculum.py
```

This checks that exactly 28 sequential Labs exist, every category and pattern
kind is valid, `confirmed_prerequisites` is empty, relation targets reference
real chapter ids, and every source file exists in the knowledge base.

## Tests

```powershell
python -m unittest discover -s tests -t . -v
```

The suite covers chapter filters, knowledge point inclusion, relation output,
missing targets, invalid inputs, and the validation script.

## Open WebUI Integration

Use the wrappers in `openwebui/`. See [docs/open-webui-integration.md](docs/open-webui-integration.md)
for step-by-step instructions. Set the Valve `COURSE_TOOLS_DIR` to the absolute
path of this `course-tools` directory.

The full input/output contract is documented in [docs/tool-contract.md](docs/tool-contract.md).

## New course extensions

### Extension 3: `course_practice_generator`

Copy `skills/course_practice_generator/SKILL.md` into Open WebUI's **Workspace > Skills**.
The Skill is intentionally grounded: it must call the existing
`course_chapter_lookup` Function before composing a question and must stop with
`课程资料中未找到/无法确认` when the chapter or evidence is unavailable. The
read-only `validate_skill.py` helper can build and inspect the same verified
context locally without turning `chapters.json` into a question bank.

### Extension 4: `course_quiz_grader`

`mcp/course_quiz_grader/server.py` is a real MCP Server and exposes
`grade_quiz_answer`. Install the exact `mcp==1.27.2` dependency in its isolated
environment and start it with Streamable HTTP:

```powershell
cd course-tools/mcp/course_quiz_grader
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py --host 127.0.0.1 --port 8001 --path /mcp
```

The Open WebUI 0.11.0 source in this project accepts this server from **Admin
Panel > Settings > Integrations > External Tool Servers**, with Type set to
**MCP Streamable HTTP** and URL `http://127.0.0.1:8001/mcp`. It does not expose a
command/stdio field for MCP. See the project-level
`新增扩展接入说明.md` for the complete click-by-click setup and the local
protocol smoke test.

## Supplied checkout name note

The supplied archive names the knowledge-base sibling directory
`python-design-pattern-rag-main`, while the existing validation script's
default is `python-design-pattern-rag`. The existing tool behavior is left
unchanged. When validating this extracted copy, pass the actual checkout
explicitly:

```powershell
python scripts/validate_curriculum.py --repo-root ..\python-design-pattern-rag-main
```
