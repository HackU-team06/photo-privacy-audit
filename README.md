# 内容
## app
- 主にPythonアプリケーション
- apiサーバー, バックエンドworker, 画像解析等
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
- `localhost:80000`: nginx
- `localhost:80001`: fastAPI
  - `localhost:80001/docs`: Swagger (APIデバッガー)
- `localhost:5556`: Celeryのタスクダッシュボード
