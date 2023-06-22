from models import AnalyzeResult
from .base import BackgroundAnalyzeProcessBase
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results, Boxes
from typing import Iterable
from PIL import Image


class YoloAnalyze(BackgroundAnalyzeProcessBase):
    def __init__(self, model_path: str) -> None:
        self.model_path = model_path

    def run(self, image_path: str, begin_num: int) -> list[list[int]]:
        # モデルの関数作成(YOLO)
        model = YOLO(self.model_path)
        # YOLO-customから座標データを抽出(YOLO)
        result: Results = model(Image.open(image_path), conf=0.25)[0]
        # 後のオブジェクト名出力などのため
        names = result.names
        classes = result.boxes.cls
        boxes: Iterable[Boxes] = result.boxes
        # 検出したオブジェクトのバウンディングボックス座標とオブジェクト名を取得し、ターミナルに出力
        output = []

        for box, cls in zip(boxes, classes):
            name = names[int(cls)]
            x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
            output.append([int(cls) + begin_num, x1, y1, x2, y2])  # 配列に保存

        return output
