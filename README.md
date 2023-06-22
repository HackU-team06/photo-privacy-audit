# 内容
## app
- 主にPythonアプリケーション
- APIサーバー(fastAPI), バックエンドワーカー(Celery), 画像解析等
## nginx
- nginxのconfig
- 静的ホストとルーティング
## www
- 静的ファイル
- 構造を保ったままnginxにホストされる
## .env
- 環境変数定義
## docker-compose.yml
- docker-compose.ymlは開発環境, docker-compose-product.ymlは本番環境

# 開発
1. `docker compose up -d --build` でcompose起動
1. 起動中のコンテナをvscodeにアタッチ
1. `docker compose reload {service_name}` でコンテナ再起動
- http://localhost:8000 : nginx (フロントエンド)
  - http://localhost:8000/api : fastAPIにリバースプロキシ
  - http://localhost:8000/docs/swagger : Swagger (APIデバッガー)
  - http://localhost:8000/docs/redoc : ReDoc (APIドキュメント)
- http://localhost:8001 : fastAPI
- http://localhost:5556: Celeryのタスクダッシュボード
