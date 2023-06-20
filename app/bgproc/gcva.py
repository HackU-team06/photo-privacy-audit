from app.models import AnalyzeResult
from base import BackgroundAnalyzeProcessBase

class GcvaAnalyze(BackgroundAnalyzeProcessBase):
    def __init__(self, json_path: str) -> None:
        self.json_path = json_path

    def run(self, image_path: str) -> list[AnalyzeResult]:
        ...

