# Open WebUI Functions Integration

The two tools are exposed as Open WebUI Functions (pipe type). They load the
local JSON files and execute real queries; no answer is embedded in the prompt.

## Prerequisites

- Open WebUI is running with Plugins enabled.
- The `course-tools` project directory is accessible from the Open WebUI process.
- The clone of `python-design-pattern-rag` stays unchanged next to `course-tools`.

## Add A Function

1. Open **Admin Panel > Functions**.
2. Click **Add Function**, choose a name such as `course_chapter_lookup`.
3. Paste the full content of `openwebui/course_chapter_lookup.py`.
4. Set the Valve `COURSE_TOOLS_DIR` to the absolute path of `course-tools`, for
   example `D:\Focusly\course-tools`.
5. Save and enable the function.

Repeat the same steps for `openwebui/course_prerequisite_lookup.py`.

The wrapper first checks `Valves.COURSE_TOOLS_DIR`, then the environment variable
`COURSE_TOOLS_DIR`, then common local candidates. If none contain
`data/chapters.json` (or `data/prerequisites.json`), the function returns a
`CONFIGURATION_ERROR` instead of guessing.

## How Invocation Works

The wrapper accepts either structured arguments or a plain user message.

Structured arguments:

```json
{
  "arguments": {
    "query": "Observer",
    "include_knowledge_points": true
  }
}
```

```json
{
  "arguments": {
    "target": "Singleton",
    "direction": "all"
  }
}
```

Message fallback: when `body.messages` is present and no explicit argument is
given, the wrapper uses the latest user message text as the `query` (chapter
tool) or `target` (prerequisite tool). The returned answer still comes from the
JSON lookup, not from the model.

## Example Result

Chapter tool request:

```json
{"arguments": {"query": "Facade"}}
```

Response:

```json
{
  "ok": true,
  "query": "Facade",
  "count": 1,
  "results": [
    {
      "id": "lab-23-facade",
      "lab_no": 23,
      "title": {"en": "Facade", "zh": "外观模式"},
      "category": "structural",
      "pattern_kind": "gof",
      "sources": ["labs/structural_facade.md", "..."]
    }
  ],
  "warnings": []
}
```

## Keeping The Tools Testable

The query logic lives in `src/course_tools/`, which is covered by `unittest`.
The Open WebUI wrappers are thin adapters that only add `src` to `sys.path` and
parse arguments. This keeps the data layer independently testable outside the
Open WebUI runtime.

