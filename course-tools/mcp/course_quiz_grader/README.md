# course_quiz_grader MCP Server

扩展 4 是一个真正可启动的 MCP Server。它只接收题目、题型、标准答案和学生答案，判分由 `grader.py` 的确定性 Python 代码完成，不依赖大模型判断。Server 使用当前项目已经锁定的 `mcp==1.27.2`，并且只提供 Open WebUI 0.11.0 能直接连接的 Streamable HTTP transport。

## 文件

- `grader.py`：无第三方依赖的归一化和判分核心。
- `server.py`：FastMCP Server，暴露 `grade_quiz_answer`。
- `smoke_test.py`：使用同一个 MCP SDK 通过 Streamable HTTP 做真实协议调用。
- `requirements.txt`：精确依赖版本。

## Windows 安装和启动

在本目录打开 PowerShell：

```powershell
cd <项目目录>\course-tools\mcp\course_quiz_grader
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py --host 127.0.0.1 --port 8001 --path /mcp
```

如果系统没有 `py -3.12`，可以把第一行替换成已安装的 Python 3.11/3.12：

```powershell
python -m venv .venv
```

成功启动时应看到 FastMCP/Uvicorn 的服务启动日志，至少包含类似：

```text
Uvicorn running on http://127.0.0.1:8001
```

实际 MCP endpoint 是：`http://127.0.0.1:8001/mcp`。不要把 `server.py` 当成 stdio 程序，也不要在 Open WebUI 的 MCP 表单中填写 command；当前 Open WebUI 源码的 MCP 客户端只实现 Streamable HTTP。

## MCP Tool schema

```json
{
  "name": "grade_quiz_answer",
  "description": "Deterministically grade one choice, multiple-choice, or true/false item.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "question": { "type": "string" },
      "question_type": { "type": "string" },
      "standard_answer": { "type": "string" },
      "student_answer": { "type": "string" },
      "explanation": { "type": "string", "default": "" },
      "source": { "type": "string", "default": "" }
    },
    "required": ["question", "question_type", "standard_answer", "student_answer"]
  }
}
```

支持的题型和归一化规则：

- 单选：`choice`、`single_choice`、选择题；接受 `A`、`a`、`A.` 等形式；
- 判断：`true_false`、判断题；接受 `对/错`、`正确/错误`、`True/False`、`T/F`、`是/否`；
- 多选：`multiple_choice`、多选题；`A,C`、`C、A`、`AC` 会转为集合后比较，顺序不影响结果；
- 空学生答案得分 0；缺标准答案、非法答案和不支持题型返回 `ok: false` 及错误码。

## 本地协议调用

启动 Server 后，在第二个 PowerShell 窗口运行：

```powershell
.\.venv\Scripts\python.exe smoke_test.py --standard-answer B --student-answer b.
```

成功调用的关键结果应类似：

```json
{
  "tool_found": true,
  "is_error": false,
  "content": [
    {
      "ok": true,
      "correct": true,
      "score": 1,
      "max_score": 1,
      "student_answer": "b.",
      "standard_answer": "B"
    }
  ]
}
```

错误输入仍应通过 MCP 返回结构化结果。例如：

```powershell
.\.venv\Scripts\python.exe smoke_test.py --question-type code_reading --standard-answer B --student-answer B
```

结果中的 `content[0].ok` 应为 `false`，`error.code` 为 `UNSUPPORTED_QUESTION_TYPE`。这不是把错误吞掉，而是 Server 明确拒绝不支持的题型。

