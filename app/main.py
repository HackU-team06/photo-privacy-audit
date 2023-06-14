import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.encoders import jsonable_encoder
from celery.result import AsyncResult

from models import *
from tasks import analyze_task

app = FastAPI(debug=True)


@app.post("/api/analyze", response_model=AnalyzeTaskStatus)
async def request_analyze(req: AnalyzeTaskRequest = Body(...), upload_file: UploadFile = File(...)) -> AnalyzeTaskStatus:
    """
    画像解析タスクのリクエスト

    configを含むリクエストと画像ファイルのアップロードをする

    タスクIDを含むステータスを返す
    """
    
    # アップロード画像を一時ファイルに保存
    fileobj = upload_file.file
    fd, path = tempfile.mkstemp(dir="/app/upload")
    with os.fdopen(fd, "wb") as f:
        shutil.copyfileobj(fileobj, f)
    
    # configと画像パスからAnalyzeTaskTaskRequestWithPathを作成
    req_with_path = AnalyzeTaskTaskRequestWithPath(config=req.config, path=path)

    # バックグラウンドタスク analyze_task を作成
    # jsonable_encoderが必要
    task = analyze_task.delay(jsonable_encoder(req_with_path))

    # タスクIDとステータスを返す
    status = AnalyzeTaskStatus(id=task.id, status=task.status)
    return status


@app.get("/api/analyze/{task_id}", response_model=AnalyzeTaskStatus)
async def check_analyze_status(task_id: str) -> AnalyzeTaskStatus:
    """
    画像解析タスクのステータスをチェックする
    終了していればresultが入っている
    """
    
    task = AsyncResult(task_id)
    status = AnalyzeTaskStatus(id=task_id, status=task.status, result=task.result)
    return status
