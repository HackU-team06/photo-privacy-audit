import uuid
from pydantic import BaseModel, Field, UUID4, BaseModel, validator
from pydantic.dataclasses import dataclass
from typing import Optional, Literal, Any, Union, Annotated
from pathlib import Path


class AnalyzeTaskConfig(BaseModel):
    """解析の設定"""
    
    foo: bool = Field(True, description="設定項目例 (default: True)")
    bar: int = Field(0, description="設定項目例 (default: 0)")
    baz: str = Field('', description="設定項目例 (default: 空文字)")


class AnalyzeTaskRequestBase(BaseModel):
    """解析のリクエストのベース"""

    config: AnalyzeTaskConfig = Field(..., description="解析の設定")


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

    path: Path = Field(..., description="画像ファイルのパス")


class BoundingBox(BaseModel):
    """バウンディングボックス"""
    
    x: int = Field(..., description="左上のx座標")
    y: int = Field(..., description="左上のy座標")
    w: int = Field(..., description="幅")
    h: int = Field(..., description="高さ")


class AnalyzeResult(BaseModel):
    """解析結果要素"""
    
    id: UUID4 = Field(default_factory=uuid.uuid4, description="ID")
    bounding_box: BoundingBox = Field(..., description="バウンディングボックス")
    name: str = Field(..., description="名前(ラベル, 種類)")
    description: str = Field(..., description="説明")
    rate: float = Field(..., description="危険度")


class AnalyzeResultList(BaseModel):
    """解析結果リスト"""

    __root__: list[AnalyzeResult]
    
    def __iter__(self):
        return iter(self.__root__)


TaskStatusLiteral = Literal[
    "PENDING", "RECEIVED", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED"
]


class TaskStatus(BaseModel):
    """タスクのステータス"""
    
    id: UUID4 = Field(..., description="ID")
    status: TaskStatusLiteral = Field(..., description="ステータス")
    result: Optional[Any] = Field(None, description="結果")


class AnalyzeTaskStatus(BaseModel):
    """解析タスクのステータス"""

    id: UUID4 = Field(..., description="ID")
    status: TaskStatusLiteral = Field(..., description="ステータス")
    result: Optional[Union[AnalyzeResultList,list[AnalyzeResult]]] = Field(None, description="結果")
