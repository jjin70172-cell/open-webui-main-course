"""Deterministic grading logic for objective course questions.

The MCP transport is kept out of this module so the important grading rules
can be exercised with the Python standard library alone.  The model supplies
the standard answer; it never decides whether the answers match.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any


SUPPORTED_QUESTION_TYPES = {
    "choice",
    "single_choice",
    "multiple_choice",
    "true_false",
}

QUESTION_TYPE_ALIASES = {
    "choice": "choice",
    "single": "choice",
    "single choice": "choice",
    "single_choice": "choice",
    "single-choice": "choice",
    "选择": "choice",
    "选择题": "choice",
    "单选": "choice",
    "单选题": "choice",
    "multiple": "multiple_choice",
    "multi": "multiple_choice",
    "multiple choice": "multiple_choice",
    "multiple_choice": "multiple_choice",
    "multiple-choice": "multiple_choice",
    "多选": "multiple_choice",
    "多选题": "multiple_choice",
    "true false": "true_false",
    "true_false": "true_false",
    "true-false": "true_false",
    "true/false": "true_false",
    "tf": "true_false",
    "判断": "true_false",
    "判断题": "true_false",
}

TRUE_VALUES = {"对", "正确", "true", "t", "yes", "y", "是", "√", "✓", "✔"}
FALSE_VALUES = {"错", "错误", "false", "f", "no", "n", "否", "×", "✗", "✘"}

_CHOICE_ALLOWED = re.compile(
    r"^[A-Za-z\s,，、;；/|+&.。:：()（）\[\]{}\-_答案选项选择选正确为是和或以及及]+$"
)
_CHOICE_SPLIT = re.compile(r"[\s,，、;；/|+&.。:：()（）\[\]{}\-_]+")
_CHOICE_LABELS = re.compile(
    r"(?i)\b(?:answer|option|options|the|correct|is|are)\b|答案|正确答案|选项|选择答案|选择|选|正确|为|是|和|或|以及|及"
)
_TF_PREFIX = re.compile(r"(?i)^(?:answer|option|答案|选项|选择)\s*[:：]?\s*")


class GradingError(ValueError):
    """A user-facing validation or normalization error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def normalize_question_type(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GradingError("INVALID_INPUT", "question_type 不能为空。")
    key = " ".join(value.strip().lower().replace("_", " ").split())
    canonical = QUESTION_TYPE_ALIASES.get(key) or QUESTION_TYPE_ALIASES.get(value.strip().lower())
    if canonical is None:
        raise GradingError(
            "UNSUPPORTED_QUESTION_TYPE",
            "仅支持选择题、单选题、多选题和判断题。",
        )
    return canonical


def _display_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() if isinstance(item, str) else item for item in value]
    return value


def _is_empty_answer(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, set)):
        return len(value) == 0
    return False


def _ensure_optional_text(value: Any, field_name: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise GradingError("INVALID_INPUT", f"{field_name} 必须是字符串。")
    return value.strip()


def _choice_tokens(value: Any) -> set[str]:
    values: Iterable[Any]
    if isinstance(value, (list, tuple, set)):
        values = value
    else:
        values = [value]

    tokens: set[str] = set()
    for item in values:
        if not isinstance(item, str):
            raise GradingError("INVALID_ANSWER_FORMAT", "选择题答案必须是 A-Z 选项字母或其分隔形式。")
        raw = item.strip()
        if not raw:
            continue
        if not _CHOICE_ALLOWED.fullmatch(raw):
            raise GradingError(
                "INVALID_ANSWER_FORMAT",
                "选择题答案包含无法识别的字符；请使用 A、B、A,C 或 A、C 形式。",
            )
        clean = _CHOICE_LABELS.sub(" ", raw)
        pieces = [piece for piece in _CHOICE_SPLIT.split(clean.upper()) if piece]
        if not pieces:
            continue
        for piece in pieces:
            if not re.fullmatch(r"[A-Z]+", piece):
                raise GradingError(
                    "INVALID_ANSWER_FORMAT",
                    "选择题答案只能包含 A-Z 选项字母。",
                )
            if len(piece) == 1:
                tokens.add(piece)
            elif len(piece) <= 8 and len(set(piece)) == len(piece):
                # Accept compact multi-select forms such as AC or ACD.
                tokens.update(piece)
            else:
                raise GradingError(
                    "INVALID_ANSWER_FORMAT",
                    "无法识别连续选项；请使用 A,C 或 A、C 形式。",
                )
    return tokens


def _true_false_value(value: Any) -> str:
    if not isinstance(value, str):
        raise GradingError("INVALID_ANSWER_FORMAT", "判断题答案必须是对/错或 True/False。")
    clean = _TF_PREFIX.sub("", value.strip()).strip(" \t\r\n.,。:：;；()（）[]{}")
    lower = clean.lower()
    if lower in TRUE_VALUES:
        return "true"
    if lower in FALSE_VALUES:
        return "false"
    raise GradingError(
        "INVALID_ANSWER_FORMAT",
        "判断题答案只能使用对/错、正确/错误、True/False、T/F 或是/否。",
    )


def _base_result(
    *,
    question: Any,
    question_type: Any,
    standard_answer: Any,
    student_answer: Any,
    explanation: Any,
    source: Any,
) -> dict[str, Any]:
    return {
        "ok": True,
        "correct": False,
        "score": 0,
        "max_score": 1,
        "question": _display_value(question),
        "question_type": _display_value(question_type),
        "student_answer": _display_value(student_answer),
        "standard_answer": _display_value(standard_answer),
        "feedback": "",
        "explanation": _display_value(explanation),
        "source": _display_value(source),
    }


def _error_result(
    *,
    code: str,
    message: str,
    question: Any,
    question_type: Any,
    standard_answer: Any,
    student_answer: Any,
    explanation: Any,
    source: Any,
) -> dict[str, Any]:
    result = _base_result(
        question=question,
        question_type=question_type,
        standard_answer=standard_answer,
        student_answer=student_answer,
        explanation=explanation,
        source=source,
    )
    result["ok"] = False
    result["feedback"] = message
    result["error"] = {"code": code, "message": message}
    return result


def _feedback(correct: bool, question_type: str, explanation: str, source: str, empty: bool = False) -> str:
    if empty:
        message = "未作答，得分 0/1。"
    elif correct:
        message = "判分结果：正确，得分 1/1。"
    elif question_type == "multiple_choice":
        message = "判分结果：不正确；选择集合与标准答案不一致，得分 0/1。"
    else:
        message = "判分结果：不正确，得分 0/1。"
    if explanation:
        message += f" 说明：{explanation}"
    if source:
        message += f" 来源：{source}"
    return message


def grade_quiz_answer(
    question: str,
    question_type: str,
    standard_answer: str,
    student_answer: str,
    explanation: str | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    """Grade one objective question without model-based judgement.

    ``question`` is required for traceability even though matching only uses
    the supplied standard and student answers.  All invalid inputs return a
    structured error instead of failing silently.
    """

    try:
        question_text = _ensure_optional_text(question, "question")
        if not question_text:
            raise GradingError("INVALID_INPUT", "question 不能为空。")
        explanation_text = _ensure_optional_text(explanation, "explanation")
        source_text = _ensure_optional_text(source, "source")
        canonical_type = normalize_question_type(question_type)
    except GradingError as exc:
        return _error_result(
            code=exc.code,
            message=exc.message,
            question=question,
            question_type=question_type,
            standard_answer=standard_answer,
            student_answer=student_answer,
            explanation=explanation,
            source=source,
        )

    result = _base_result(
        question=question_text,
        question_type=canonical_type,
        standard_answer=standard_answer,
        student_answer=student_answer,
        explanation=explanation_text,
        source=source_text,
    )

    if _is_empty_answer(standard_answer):
        return _error_result(
            code="MISSING_STANDARD_ANSWER",
            message="缺少标准答案，无法进行确定性判分。",
            question=question_text,
            question_type=canonical_type,
            standard_answer=standard_answer,
            student_answer=student_answer,
            explanation=explanation_text,
            source=source_text,
        )

    try:
        if canonical_type == "true_false":
            normalized_standard: Any = _true_false_value(standard_answer)
        else:
            normalized_standard = _choice_tokens(standard_answer)
            if canonical_type == "choice" and len(normalized_standard) != 1:
                raise GradingError("INVALID_STANDARD_ANSWER", "单选题标准答案必须恰好包含一个选项。")
    except GradingError as exc:
        return _error_result(
            code=exc.code if exc.code.startswith("INVALID_STANDARD") else "INVALID_STANDARD_ANSWER",
            message=exc.message,
            question=question_text,
            question_type=canonical_type,
            standard_answer=standard_answer,
            student_answer=student_answer,
            explanation=explanation_text,
            source=source_text,
        )

    if _is_empty_answer(student_answer):
        result["normalized_standard_answer"] = (
            normalized_standard if canonical_type == "true_false" else sorted(normalized_standard)
        )
        result["normalized_student_answer"] = None
        result["feedback"] = _feedback(False, canonical_type, explanation_text, source_text, empty=True)
        return result

    try:
        if canonical_type == "true_false":
            normalized_student: Any = _true_false_value(student_answer)
        else:
            normalized_student = _choice_tokens(student_answer)
            if canonical_type == "choice" and len(normalized_student) != 1:
                raise GradingError("INVALID_STUDENT_ANSWER", "单选题学生答案必须恰好包含一个选项。")
    except GradingError as exc:
        return _error_result(
            code=exc.code if exc.code.startswith("INVALID_STUDENT") else "INVALID_STUDENT_ANSWER",
            message=exc.message,
            question=question_text,
            question_type=canonical_type,
            standard_answer=standard_answer,
            student_answer=student_answer,
            explanation=explanation_text,
            source=source_text,
        )

    correct = normalized_student == normalized_standard
    result["correct"] = correct
    result["score"] = 1 if correct else 0
    result["normalized_standard_answer"] = (
        normalized_standard if canonical_type == "true_false" else sorted(normalized_standard)
    )
    result["normalized_student_answer"] = (
        normalized_student if canonical_type == "true_false" else sorted(normalized_student)
    )
    result["feedback"] = _feedback(correct, canonical_type, explanation_text, source_text)
    return result


# A descriptive alias is useful for direct Python callers while the MCP tool
# keeps the concise name ``grade_quiz_answer``.
grade_objective_question = grade_quiz_answer
