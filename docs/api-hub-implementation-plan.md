## api-hub 実装計画

### 実装ステップ

#### Step 1: プロジェクトセットアップ ✅

- [x] `pyproject.toml` 作成（uv、依存パッケージの定義）
- [x] `.env.example` 作成
- [x] `.gitignore` に `.env` を追加
- [x] ディレクトリ構成の作成

**依存パッケージ**

| パッケージ | 用途 |
|---|---|
| `fastapi` | Webフレームワーク |
| `uvicorn` | ASGIサーバ |
| `httpx` | 非同期HTTPクライアント |
| `python-dotenv` | `.env` 読み込み |
| `pydantic` | スキーマ定義・バリデーション |

**開発用パッケージ**

| パッケージ | 用途 |
|---|---|
| `ruff` | Linter/Formatter |
| `mypy` | 型チェック |
| `pytest` | テスト |
| `pytest-asyncio` | 非同期テスト |

---

#### Step 2: スキーマ定義（`app/schemas/book.py`） ✅

レスポンスの型を定義する。

**`BookSummary`**（検索結果の1件）

| フィールド | 型 |
|---|---|
| `id` | `str` |
| `title` | `str` |
| `authors` | `list[str] \| None` |
| `thumbnail` | `str \| None` |
| `published_date` | `str \| None` |
| `description` | `str \| None` |

**`BookSearchResponse`**（`GET /books/search` のレスポンス）

| フィールド | 型 |
|---|---|
| `total` | `int` |
| `limit` | `int` |
| `offset` | `int` |
| `items` | `list[BookSummary]` |

**`BookDetail`**（`GET /books/{id}` のレスポンス）

`BookSummary` を継承し以下を追加：

| フィールド | 型 |
|---|---|
| `page_count` | `int \| None` |
| `categories` | `list[str] \| None` |
| `publisher` | `str \| None` |
| `isbn` | `str \| None` |

---

#### Step 3: Google Books API サービス（`app/services/google_books.py`） ✅

Google Books API の呼び出しとレスポンスの加工を担当する。

**実装する関数**

| 関数 | 内容 |
|---|---|
| `search_books(q, limit, offset)` | `GET /volumes?q=...` を呼び出し `BookSearchResponse` を返す |
| `get_book(id)` | `GET /volumes/{id}` を呼び出し `BookDetail` を返す |
| `_parse_summary(item)` | Google Books API の1件を `BookSummary` に変換 |
| `_parse_detail(item)` | Google Books API の1件を `BookDetail` に変換 |
| `_extract_isbn(identifiers)` | `industryIdentifiers` から ISBN_13 優先で抽出 |

**フィールドマッピングの注意点**

- 存在しないフィールドはすべて `None` を返す
- `isbn` は `ISBN_13` 優先、なければ `ISBN_10`、どちらもなければ `None`
- `thumbnail` は `volumeInfo.imageLinks.thumbnail` を使用

---

#### Step 4: ルーター（`app/routers/books.py`） ✅

| エンドポイント | 処理 |
|---|---|
| `GET /books/search` | `q` が空なら 400 を返す。`search_books()` を呼び出して返す |
| `GET /books/{id}` | `get_book()` を呼び出す。見つからなければ 404 を返す |

---

#### Step 5: エントリーポイント（`app/main.py`） ✅

- FastAPI インスタンスの作成
- ルーターの登録
- 環境変数（`GOOGLE_BOOKS_API_KEY`）の読み込み

---

#### Step 6: テスト（`tests/`） ✅

| テスト対象 | 内容 |
|---|---|
| `_parse_summary()` | フィールドの正常マッピング、`None` の挙動 |
| `_extract_isbn()` | ISBN_13 優先、ISBN_10 フォールバック、どちらもない場合 |
| `GET /books/search` | 正常系、`q` が空の場合（400） |
| `GET /books/{id}` | 正常系、存在しない ID（404） |

---

### ディレクトリ構成

```
api-hub/
├── app/
│   ├── main.py
│   ├── routers/
│   │   └── books.py
│   ├── services/
│   │   └── google_books.py
│   └── schemas/
│       └── book.py
├── tests/
│   ├── test_services.py
│   └── test_routers.py
├── .env
├── .env.example
├── pyproject.toml
└── README.md
```

---

### 実装順序

```
Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6
セットアップ  スキーマ   サービス   ルーター   エントリー  テスト
```

依存関係があるため上から順に実装する。
