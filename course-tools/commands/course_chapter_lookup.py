"""Command line entry point for the course chapter lookup tool."""

import argparse
import json
import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from course_tools.chapters import course_chapter_lookup  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query the local course curriculum index (chapters.json)."
    )
    parser.add_argument("--query", help="Free-text query against title, alias, keyword, or summary.")
    parser.add_argument("--category", choices=["behavioral", "creational", "structural"])
    parser.add_argument("--lab-no", type=int, dest="lab_no", help="Filter by 1-based Lab number.")
    parser.add_argument(
        "--pattern-kind",
        choices=["gof", "python_idiom", "architecture"],
        help="Filter by pattern family.",
    )
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results.")
    parser.add_argument(
        "--include-knowledge-points",
        action="store_true",
        help="Include the knowledge points in each result.",
    )
    parser.add_argument(
        "--no-sources",
        action="store_true",
        help="Omit source file paths from results.",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Knowledge base repository root used for source existence checks.",
    )
    return parser


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = build_parser().parse_args(argv)
    result = course_chapter_lookup(
        query=args.query,
        category=args.category,
        lab_no=args.lab_no,
        pattern_kind=args.pattern_kind,
        limit=args.limit,
        include_knowledge_points=args.include_knowledge_points,
        include_sources=not args.no_sources,
        repo_root=args.repo_root,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
