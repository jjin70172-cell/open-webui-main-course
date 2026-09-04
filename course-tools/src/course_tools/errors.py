"""Shared error types for the course curriculum tools."""


class CourseToolsError(Exception):
    """Base error with a stable machine-readable code."""

    def __init__(self, code: str, message: str, *, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict:
        payload = {
            "code": self.code,
            "message": self.message,
        }
        if self.details:
            payload["details"] = self.details
        return payload


class DataFileNotFoundError(CourseToolsError):
    def __init__(self, path: str):
        super().__init__("DATA_FILE_NOT_FOUND", f"课程数据文件未找到: {path}", details={"path": path})


class DataSchemaError(CourseToolsError):
    def __init__(self, message: str, *, details=None):
        super().__init__("DATA_SCHEMA_ERROR", message, details=details)


class InvalidInputError(CourseToolsError):
    def __init__(self, message: str):
        super().__init__("INVALID_INPUT", message)


class EntityNotFoundError(CourseToolsError):
    def __init__(self, entity: str, *, candidates=None):
        details = {"entity": entity}
        if candidates:
            details["candidates"] = candidates
        super().__init__("ENTITY_NOT_FOUND", f"本地课程索引未找到该知识点: {entity}", details=details)


class AmbiguousQueryError(CourseToolsError):
    def __init__(self, message: str, *, candidates=None):
        super().__init__("AMBIGUOUS_QUERY", message, details={"candidates": candidates or []})


class CycleDetectedError(CourseToolsError):
    def __init__(self, path):
        super().__init__("CYCLE_DETECTED", "先修关系图检测到环。", details={"path": path})


class UnknownError(CourseToolsError):
    def __init__(self, message: str):
        super().__init__("UNKNOWN_ERROR", message)

