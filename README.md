# api-hub

Google Books API へのリクエストを中継・加工して返す共通APIサーバ。

## 技術スタック

| 項目 | 内容 |
|---|---|
| 言語 | Python 3.12+ |
| フレームワーク | FastAPI |
| パッケージ管理 | uv |
| HTTPクライアント | httpx |

## セットアップ

```bash
# 1. 環境変数ファイルを作成
cp .env.example .env

# 2. .env に APIキーを設定
# GOOGLE_BOOKS_API_KEY=your_api_key_here

# 3. 依存パッケージをインストール
uv sync
```

Google Books API キーは [Google Cloud Console](https://console.cloud.google.com/) から取得できます。

## 起動

```bash
uv run uvicorn app.main:app --reload
```

`http://localhost:8000/docs` で Swagger UI を確認できます。

## API エンドポイント

### `GET /books/search` — 本の検索

**クエリパラメータ**

| パラメータ | 必須 | デフォルト | 説明 |
|---|---|---|---|
| `q` | ✅ | - | 検索キーワード |
| `limit` | ❌ | 10 | 取得件数（最大40） |
| `offset` | ❌ | 0 | 取得開始位置 |

```bash
curl "http://localhost:8000/books/search?q=Python"
```

### `GET /books/{id}` — 本の詳細取得

```bash
curl "http://localhost:8000/books/xxxxxx"
```

## テスト

```bash
uv run pytest tests/ -v
```

## ディレクトリ構成

```
api-hub/
├── app/
│   ├── main.py                   # エントリーポイント
│   ├── routers/
│   │   └── books.py              # /books エンドポイント
│   ├── services/
│   │   └── google_books.py       # Google Books API 呼び出し・加工
│   └── schemas/
│       └── book.py               # レスポンスの型定義
├── tests/
│   ├── test_services.py
│   └── test_routers.py
├── docs/                         # 設計ドキュメント
├── .env.example
└── pyproject.toml
```
