from models import AnalyzeResult
from .base import BackgroundAnalyzeProcessBase
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results, Boxes
from typing import Iterable
from PIL import Image


class YoloAnalyze(BackgroundAnalyzeProcessBase):
    def __init__(self, model_path: str) -> None:
        self.model_path = model_path

    def run(self, image_path: str) -> list[AnalyzeResult]:
        # モデルの関数作成(YOLO)
        model = YOLO(self.model_path)
        # YOLO-customから座標データを抽出(YOLO)
        result: Results = model(Image.open(image_path), conf=0.25, iou=0.7)[0]
        # 後のオブジェクト名出力などのため
        names: dict[int, str] = result.names
        classes = result.boxes.cls
        boxes: Iterable[Boxes] = result.boxes

        result_list = []
        for box, cls_idx in zip(boxes, classes):
            if not isinstance(box, Boxes):
                continue
            name = names[int(cls_idx)].replace("_", " ")
            x1, y1, x2, y2 = (int(i) for i in box.xyxy[0])
            x, y, w, h = x1, y1, x2-x1, y2-y1
            conf = float(box.conf)
            result_list.append(AnalyzeResult(
                bounding_box={"x": x, "y": y, "w": w, "h": h},
                name=name,
                description=name,
                confidence=conf
            ))

        return result_list
