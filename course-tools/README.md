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

