from app.models import AnalyzeResult
from base import BackgroundAnalyzeProcessBase

class YoloAnalyze(BackgroundAnalyzeProcessBase):
    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
    

    def run(self, image_path: str) -> list[AnalyzeResult]:
        ...

