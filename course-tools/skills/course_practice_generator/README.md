# course_practice_generator

这是扩展 3 的 Open WebUI Skill。它不是把一段提示词伪装成函数：运行时必须先调用现有的、读取 `course-tools/data/chapters.json` 的 `course_chapter_lookup` Tool，再让模型依据返回的结构化章节事实组织题目。`validate_skill.py` 还提供一个无第三方依赖的本地核验入口，用于检查章节选择、题型/难度参数、来源路径和“资料正文缺失”情况。

## 文件

- `SKILL.md`：复制到 Open WebUI 的 Skills 编辑器；包含触发条件、数据边界和输出契约。
- `validate_skill.py`：只读读取 `../data/chapters.json`，生成已核验上下文包；不会生成课程事实，也不会修改数据。
- `__init__.py`：让测试和脚本导入路径稳定。

## 本地核验

在 `course-tools` 目录运行：

```powershell
python skills/course_practice_generator/validate_skill.py --lab-no 11 --difficulty 中等 --question-type choice --question-type code_reading --count 5
```

这条命令的输出是给 Skill 使用的“证据上下文”，不是 Open WebUI 聊天结果。找不到章节时命令以非零状态退出，并返回明确的错误码。

## Open WebUI 中的运行依赖

Skill 本身不执行 Python 脚本；它通过 Open WebUI 的 Skill 机制要求模型调用现有 `course_chapter_lookup` Tool。因此需要同时：

1. 保持已有 `course_chapter_lookup` Function 已启用，并把 `COURSE_TOOLS_DIR` 指向本目录的 `course-tools`；
2. 在 Workspace > Skills 中创建本 Skill；
3. 在课程专属模型的编辑页同时绑定本 Skill 和已有的 `course_chapter_lookup` Tool。

如果聊天中工具未出现在模型可用工具列表，Skill 必须报告无法核验，而不是退回到模型常识出题。

