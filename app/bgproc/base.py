from models import AnalyzeResult

class BackgroundAnalyzeProcessBase():
    def __init__(self) -> None:
        pass
    
    def run(self, image_path: str) -> list[AnalyzeResult]:
        pass
