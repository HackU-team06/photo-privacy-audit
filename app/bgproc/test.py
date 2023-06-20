# GCVA_YOLOのmain処理みたいな単体テスト等はココで実行する
from . import YoloAnalyze
from . import GcvaAnalyze
from models import AnalyzeResult


def main() -> list[AnalyzeResult]:
    # 身元証明書のjson path
    JSON_PATH = "/app/bgproc/content/google_cloud_account_service.json"
    # The name of the image file to annotate
    IMG_PATH = "/app/bgproc/content/IMG_6407.jpg"
    ORIGINAL_MODEL = "yolov8n.pt"
    CUSTOM_MODEL = "/app/bgproc/content/train_model/using_model.pt"

    original_yolo = YoloAnalyze(ORIGINAL_MODEL)
    gcva = GcvaAnalyze(JSON_PATH)
    custom_yolo = YoloAnalyze(CUSTOM_MODEL)

    output = [
        *original_yolo.run(IMG_PATH),
        *gcva.run(IMG_PATH),
        *custom_yolo.run(IMG_PATH),
    ]
    return output


if __name__ == "__main__":
    main()
