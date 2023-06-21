from models import AnalyzeResult
from .base import BackgroundAnalyzeProcessBase
from ultralytics import YOLO

class YoloAnalyze(BackgroundAnalyzeProcessBase):
    def __init__(self, model_path: str) -> None:
        self.model_path = model_path

    def run(self, image_path: str,begin_num: int) -> list[AnalyzeResult]:
        # モデルの関数作成(YOLO)
        model = YOLO(self.model_path)
        #YOLO-customから座標データを抽出(YOLO)
        results = model(image_path,conf=0.25)
        result = results[0]
        # 後のオブジェクト名出力などのため
        names = results[0].names
        classes = results[0].boxes.cls
        boxes = results[0].boxes
        annotatedFrame = results[0].plot()
        # 検出したオブジェクトのバウンディングボックス座標とオブジェクト名を取得し、ターミナルに出力
        output = []

        for box, cls in zip(boxes, classes):
            name = names[int(cls)]
            x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
            output.append([int(cls)+begin_num,x1,y1,x2,y2])#配列に保存

        return (output) 


