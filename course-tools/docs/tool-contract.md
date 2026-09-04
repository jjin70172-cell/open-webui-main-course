# Tool Contract

This document defines the data files and the stable input/output contract for the
two course tools. The tools are real data query utilities: they load the local
JSON index and search it. They do not generate course content from a model, and
they do not embed answers in a prompt.

## Data Files

Both files live under `data/` and are consumed by the Python package in `src/`.

### `data/chapters.json`

Root fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Index format version. |
| `repository` | Source repository name. |
| `source_commit` | The checked-out commit the index was derived from. |
| `index_definition` | Metadata such as the Lab order source and pattern kinds. |
| `chapters` | Exactly 28 learning units ordered by `labs/index.md`. |

Each chapter:

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier such as `lab-05-observer`. |
| `lab_no` | One-based Lab number, 1 through 28. |
| `title.en` / `title.zh` | Original English title and Chinese display alias. |
| `aliases` | Searchable alternate names. |
| `category` | `behavioral`, `creational`, or `structural`. |
| `pattern_kind` | `gof`, `python_idiom`, or `architecture`. |
| `summary` | Short factual description taken from the source. |
| `keywords` | Search keywords. |
| `knowledge_points` | Knowledge points extracted from the Lab and lesson. |
| `sources` | Source files with their `path` and `type`. |

Each knowledge point has `id`, `type`, `text`, `source_files`, `evidence`, and
`confidence`. Allowed types are `pattern_role`, `python_technique`, `lab_task`,
`pitfall`, and `comparison`.

### `data/prerequisites.json`

| Field | Meaning |
| --- | --- |
| `foundations` | Course-level foundations, currently Python familiarity. |
| `confirmed_prerequisites` | Formal prerequisite edges. Intentionally empty. |
| `related` | Explicit comparison, alternative, or confusion relationships. |
| `unconfirmed` | Candidate orderings that are not stated as required by source. |
| `unmapped_references` | External entities mentioned but with no local module. |

Every relation carries `source_files` and `evidence` for later audit. No
question-bank fields (`options`, `correct_answer`, `score`, etc.) are present.

## Chapter Lookup

Function: `course_chapter_lookup`

Inputs:

| Parameter | Type | Description |
| --- | --- | --- |
| `query` | `str` optional | Free-text match against id, title, alias, keyword, or summary. |
| `category` | `str` optional | `behavioral`, `creational`, or `structural`. |
| `lab_no` | `int` optional | Exact Lab number filter. |
| `pattern_kind` | `str` optional | `gof`, `python_idiom`, or `architecture`. |
| `limit` | `int` | Maximum results, default 5. |
| `include_knowledge_points` | `bool` | Include knowledge points, default false. |
| `include_sources` | `bool` | Include source paths, default true. |
| `repo_root` | path optional | Override the knowledge base checkout path. |

Output:

```json
{
  "ok": true,
  "query": "Observer",
  "filters": {"category": null, "lab_no": null, "pattern_kind": null},
  "match_type": "exact",
  "matched_by": ["title.en"],
  "count": 1,
  "limit": 5,
  "results": [
    {
      "id": "lab-05-observer",
      "lab_no": 5,
      "title": {"en": "Observer", "zh": "观察者模式"},
      "category": "behavioral",
      "pattern_kind": "gof",
      "aliases": ["Observer Pattern", "观察者"],
      "summary": "...",
      "sources": ["labs/behavioral_observer.md", "..."]
    }
  ],
  "warnings": [],
  "suggestions": []
}
```

When no result is found, `ok` remains true, `count` is 0, and `suggestions`
contains candidate titles.

## Prerequisite And Relation Lookup

Function: `course_prerequisite_lookup`

Inputs:

| Parameter | Type | Description |
| --- | --- | --- |
| `target` | `str` or `int` | Chapter id, Lab number, title, alias, or knowledge point id. |
| `direction` | `str` optional | `all`, `incoming`, or `outgoing`; default `all`. |
| `max_depth` | `int` optional | Accepted for compatibility; no multi-hop traversal exists. |
| `include_related` | `bool` | Include related relations, default true. |
| `include_unconfirmed` | `bool` | Include unconfirmed relations, default true. |
| `include_foundations` | `bool` | Include foundations, default true. |
| `repo_root` | path optional | Override the knowledge base checkout path. |

Output includes `target`, `confirmed_prerequisites` (always empty), `related`,
`unconfirmed`, `foundations`, `counts`, and `warnings`. Each relation includes
its `relation_type`, `confidence`, `source_files`, and `evidence`.

`direction` only changes how directional `unconfirmed` edges are selected.
`related` edges are undirected comparisons and are always returned for a matched
chapter.

## Errors And Warnings

Errors use a stable shape:

```json
{"ok": false, "error": {"code": "INVALID_INPUT", "message": "..."}}
```

Codes:

| Code | Meaning |
| --- | --- |
| `DATA_FILE_NOT_FOUND` | A required JSON file is missing. |
| `DATA_SCHEMA_ERROR` | A JSON file is malformed or missing fields. |
| `INVALID_INPUT` | An argument has an invalid type or value. |
| `ENTITY_NOT_FOUND` | The target does not exist in the index. |
| `AMBIGUOUS_QUERY` | The target matches more than one chapter. |
| `SOURCE_FILE_MISSING` | Emitted as a warning, not an error. |
| `UNKNOWN_ERROR` | Defensive fallback. |

When a referenced source file is missing, the result is still returned and a
`SOURCE_FILE_MISSING` warning is added so the caller can audit the source.

