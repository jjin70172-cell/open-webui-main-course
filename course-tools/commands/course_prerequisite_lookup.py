"""Command line entry point for the prerequisite and related relation lookup."""

import argparse
import json
import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from course_tools.prerequisites import course_prerequisite_lookup  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query recorded prerequisite and related relations (prerequisites.json)."
    )
    parser.add_argument("target", help="Chapter id, Lab number, title, alias, or knowledge point id.")
    parser.add_argument(
        "--direction",
        choices=["all", "incoming", "outgoing"],
        default="all",
        help="Which side of the relation to return.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Accepted for API compatibility; no multi-hop traversal exists because confirmed edges are empty.",
    )
    parser.add_argument(
        "--no-related",
        action="store_true",
        help="Exclude related (comparison/alternative/confusion) relations.",
    )
    parser.add_argument(
        "--no-unconfirmed",
        action="store_true",
        help="Exclude unconfirmed candidate prerequisite relations.",
    )
    parser.add_argument(
        "--no-foundations",
        action="store_true",
        help="Exclude global foundations such as Python familiarity.",
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
    result = course_prerequisite_lookup(
        target=args.target,
        direction=args.direction,
        max_depth=args.max_depth,
        include_related=not args.no_related,
        include_unconfirmed=not args.no_unconfirmed,
        include_foundations=not args.no_foundations,
        repo_root=args.repo_root,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
