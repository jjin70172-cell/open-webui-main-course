"""MCP Streamable HTTP server for deterministic objective-question grading."""

from __future__ import annotations

import argparse
import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - exercised by setup errors
    raise SystemExit(
        "缺少 MCP 依赖，请在本目录运行：python -m pip install -r requirements.txt"
    ) from exc

from grader import grade_quiz_answer as _grade_quiz_answer


mcp = FastMCP("course_quiz_grader")


@mcp.tool()
def grade_quiz_answer(
    question: str,
    question_type: str,
    standard_answer: str,
    student_answer: str,
    explanation: str = "",
    source: str = "",
) -> dict[str, Any]:
    """Deterministically grade one choice, multiple-choice, or true/false item.

    The comparison is performed by Python code.  Accepted answer forms include
    A/a/A., 对/错, True/False, and order-independent multi-select strings such as
    A,C or C、A. Unsupported types and malformed inputs return an error object.
    """

    return _grade_quiz_answer(
        question=question,
        question_type=question_type,
        standard_answer=standard_answer,
        student_answer=student_answer,
        explanation=explanation,
        source=source,
    )


def _normalise_path(path: str) -> str:
    value = (path or "/mcp").strip()
    if not value.startswith("/"):
        value = f"/{value}"
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run course_quiz_grader as an MCP Streamable HTTP server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--path", default="/mcp", help="Streamable HTTP endpoint path")
    args = parser.parse_args(argv)

    if not 1 <= args.port <= 65535:
        parser.error("--port 必须是 1 到 65535 之间的端口。")

    # FastMCP 1.27.2 exposes these server settings and uses them when the
    # streamable-http transport is selected.
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.settings.streamable_http_path = _normalise_path(args.path)
    mcp.run(transport="streamable-http")
    return 0


if __name__ == "__main__":
    sys.exit(main())

