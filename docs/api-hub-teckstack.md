## api-hub 技術スタック

### 構成

|項目|選択|理由|
|---|---|---|
|**言語**|Python|シンプルで読みやすい|
|**フレームワーク**|FastAPI|自動ドキュメント生成・非同期対応|
|**パッケージ管理**|uv|モダンで高速|
|**HTTPクライアント**|httpx|非同期対応・FastAPIとの相性が良い|

### 開発環境

|項目|選択|
|---|---|
|**Pythonバージョン**|3.12以上|
|**リンター/フォーマッター**|Ruff|
|**型チェック**|mypy|

### 環境変数

|変数名|必須|説明|
|---|---|---|
|`GOOGLE_BOOKS_API_KEY`|✅|Google Books API のAPIキー|

- `.env` ファイル（ローカル開発）と環境変数（本番・CI）の両方に対応
- `.env` は `.gitignore` に追加し、`.env.example` をリポジトリに含める

### ディレクトリ構成（案）

```
api-hub/
├── app/
│   ├── main.py          # エントリーポイント
│   ├── routers/
│   │   └── books.py     # /books エンドポイント
│   ├── services/
│   │   └── google_books.py  # Google Books API呼び出し・加工
│   └── schemas/
│       └── book.py      # レスポンスの型定義
├── tests/
├── .env                 # APIキーなど
├── pyproject.toml       # uv管理
└── README.md
```

### 主要エンドポイント（MVP）

|メソッド|パス|内容|
|---|---|---|
|`GET`|`/books/search?q=xxx`|本を検索|
|`GET`|`/books/{id}`|本の詳細取得|