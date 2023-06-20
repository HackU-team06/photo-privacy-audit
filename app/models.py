import uuid
from pydantic import BaseModel, Field, UUID4, BaseModel, validator
from pydantic.dataclasses import dataclass
from typing import Optional, Literal, Any, Union, Annotated
from pathlib import Path


class AnalyzeTaskConfig(BaseModel):
    """解析の設定"""
    
    foo: bool = Field(default=True, description="設定項目例 (default: True)")
    bar: int = Field(default=0, description="設定項目例 (default: 0)")
    baz: str = Field(default='', description="設定項目例 (default: 空文字)")


class AnalyzeTaskRequestBase(BaseModel):
    """解析のリクエストのベース"""

    config: AnalyzeTaskConfig = Field(defautl=..., description="解析の設定")


class AnalyzeTaskFormRequest(AnalyzeTaskRequestBase):
    """解析のリクエスト (フォーム版)"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls.parse_raw(value)
        return value


class AnalyzeTaskBase64Request(AnalyzeTaskRequestBase):
    """解析のリクエスト (Base64版)"""

    encoded_file: Annotated[str, 'Base64File']


class AnalyzeTaskTaskRequestWithPath(AnalyzeTaskRequestBase):
    """解析のリクエスト (画像ファイルのパス付き)"""

    path: Path = Field(default=..., description="画像ファイルのパス")


class BoundingBox(BaseModel):
    """バウンディングボックス"""
    
    x: int = Field(default=..., description="左上のx座標")
    y: int = Field(default=..., description="左上のy座標")
    w: int = Field(default=..., description="幅")
    h: int = Field(default=..., description="高さ")


class AnalyzeResult(BaseModel):
    """解析結果要素"""
    
    id: UUID4 = Field(default_factory=uuid.uuid4, description="ID")
    bounding_box: BoundingBox = Field(default=..., description="バウンディングボックス")
    name: str = Field(default=..., description="名前(ラベル, 種類)")
    description: str = Field(default=..., description="説明")
    rate: float = Field(default=..., description="危険度")


class AnalyzeResultList(BaseModel):
    """解析結果リスト"""

    __root__: list[AnalyzeResult]


TaskStatusLiteral = Literal[
    "PENDING", "RECEIVED", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED"
]


class TaskStatus(BaseModel):
    """タスクのステータス"""
    
    id: UUID4 = Field(default=..., description="ID")
    status: TaskStatusLiteral = Field(default=..., description="ステータス")
    result: Optional[Any] = Field(default=None, description="結果")


class AnalyzeTaskStatus(BaseModel):
    """解析タスクのステータス"""

    id: UUID4 = Field(default=..., description="ID")
    status: TaskStatusLiteral = Field(default=..., description="ステータス")
    result: Optional[Union[AnalyzeResultList,list[AnalyzeResult]]] = Field(default=None, description="結果")
