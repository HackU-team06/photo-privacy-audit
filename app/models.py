import uuid
from pydantic import BaseModel, Field, UUID4, BaseModel, validator
from pydantic.dataclasses import dataclass
from typing import Optional, Literal, Any, Union, Annotated
from pathlib import Path



__all__ = [
    "AnalyzeTaskConfig",
    "AnalyzeTaskRequest",
    "AnalyzeTaskFormRequest",
    "AnalyzeTaskBase64Request",
    "AnalyzeTaskTaskRequestWithPath",
    "BoundingBox",
    "AnalyzeResult",
    "AnalyzeResultList",
    "TaskStatus",
    "AnalyzeTaskStatus",
]


class AnalyzeTaskConfig(BaseModel):
    foo: bool
    bar: int
    baz: str


class AnalyzeTaskRequest(BaseModel):
    config: AnalyzeTaskConfig


class AnalyzeTaskFormRequest(AnalyzeTaskRequest):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls.parse_raw(value)
        return value


class AnalyzeTaskBase64Request(AnalyzeTaskRequest):
    encoded_file: Annotated[str, 'Base64File']


class AnalyzeTaskTaskRequestWithPath(AnalyzeTaskRequest):
    path: Path


class BoundingBox(BaseModel):
    x: int
    y: int
    w: int
    h: int


class AnalyzeResult(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    bounding_box: BoundingBox
    name: str
    description: str


class AnalyzeResultList(BaseModel):
    __root__: list[AnalyzeResult]


TaskStatusLiteral = Literal[
    "PENDING", "RECEIVED", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED"
]


class TaskStatus(BaseModel):
    id: UUID4
    status: TaskStatusLiteral
    result: Optional[Any]


class AnalyzeTaskStatus(BaseModel):
    id: UUID4
    status: TaskStatusLiteral
    result: Optional[Union[AnalyzeResultList,list[AnalyzeResult]]]
