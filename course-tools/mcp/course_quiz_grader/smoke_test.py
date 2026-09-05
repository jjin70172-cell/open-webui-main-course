"""Small MCP client smoke test for course_quiz_grader."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def _block_to_json(block: Any) -> Any:
    if hasattr(block, "text"):
        text = block.text
        try:
            return json.loads(text)
        except (TypeError, json.JSONDecodeError):
            return text
    if hasattr(block, "model_dump"):
        return block.model_dump(mode="json")
    return str(block)


async def _run(args: argparse.Namespace) -> dict[str, Any]:
    arguments = {
        "question": args.question,
        "question_type": args.question_type,
        "standard_answer": args.standard_answer,
        "student_answer": args.student_answer,
    }
    if args.explanation:
        arguments["explanation"] = args.explanation
    if args.source:
        arguments["source"] = args.source

    async with AsyncExitStack() as stack:
        streams = await stack.enter_async_context(streamablehttp_client(args.url))
        read_stream, write_stream, _ = streams
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        tool_list = await session.list_tools()
        tool_names = [tool.name for tool in tool_list.tools]
        tool_schemas = [tool.model_dump(mode="json") for tool in tool_list.tools]
        call_result = await session.call_tool("grade_quiz_answer", arguments=arguments)
        content = [_block_to_json(block) for block in call_result.content]
        structured = getattr(call_result, "structuredContent", None)
        return {
            "url": args.url,
            "tool_names": tool_names,
            "tool_schemas": tool_schemas,
            "tool_found": "grade_quiz_answer" in tool_names,
            "is_error": bool(call_result.isError),
            "structured_content": structured,
            "content": content,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Call course_quiz_grader through MCP Streamable HTTP.")
    parser.add_argument("--url", default="http://127.0.0.1:8001/mcp")
    parser.add_argument("--question", default="抽象工厂通过什么方式创建产品族？")
    parser.add_argument("--question-type", default="choice")
    parser.add_argument("--standard-answer", default="B")
    parser.add_argument("--student-answer", default="b.")
    parser.add_argument("--explanation", default="课程资料明确区分了产品族创建方式。")
    parser.add_argument("--source", default="data/chapters.json")
    args = parser.parse_args(argv)
    result = asyncio.run(_run(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("tool_found") and not result.get("is_error") else 1


if __name__ == "__main__":
    sys.exit(main())
