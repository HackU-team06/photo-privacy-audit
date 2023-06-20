import time
from typing import cast

from celery import Celery
from celery.app.task import Task
from fastapi.encoders import jsonable_encoder
from PIL import Image

from models import AnalyzeResult, AnalyzeResultList, AnalyzeTaskTaskRequestWithPath


celery = Celery(__name__)
celery.conf.update(
    result_expires=3600,  # 結果のTTLを1時間（3600秒）に設定
)


@celery.task
def analyze(req_json: dict) -> list:
    """
    画像を解析するバックグラウンドタスク

    引数、返り値はシリアライズのためjsonable_encoderをかける

    Args:
        req_with_path_json: jsonable_encoder(AnalyzeTaskTaskRequestWithPath)

    Returns:
        list: jsonable_encoder(AnalyzeResultList)
    """

    time.sleep(10)  # 動作確認のためのsleep

    try:
        req = AnalyzeTaskTaskRequestWithPath(**req_json)
        img = Image.open(req.path)
        results: AnalyzeResultList = [
            AnalyzeResult(
                bounding_box={"x": 1, "y": 2, "w": 3, "h": 4},
                name="sample",
                description="sample result",
            )
        ]
    finally:
        if req.path.exists():
            req.path.unlink()
    return jsonable_encoder(results)


# Task にキャストしたもの
analyze_task = cast(Task, analyze)
