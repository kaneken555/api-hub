## api-hub API仕様

### 共通

|項目|内容|
|---|---|
|**ベースURL**|`http://localhost:8000` （開発時）|
|**レスポンス形式**|JSON|
|**文字コード**|UTF-8|

---

### エンドポイント一覧

#### `GET /books/search` — 本の検索

**クエリパラメータ**

|パラメータ|必須|型|説明|
|---|---|---|---|
|`q`|✅|string|検索キーワード|
|`limit`|❌|integer|取得件数（デフォルト: 10、最大: 40）|
|`offset`|❌|integer|取得開始位置（デフォルト: 0）|

**レスポンス**

json

```json
{
  "total": 100,
  "limit": 10,
  "offset": 0,
  "items": [
    {
      "id": "xxxxxx",
      "title": "本のタイトル",
      "authors": ["著者名"],
      "thumbnail": "https://...",
      "published_date": "2024-01-01",
      "description": "概要テキスト"
    }
  ]
}
```

---

#### `GET /books/{id}` — 本の詳細取得

**パスパラメータ**

|パラメータ|必須|型|説明|
|---|---|---|---|
|`id`|✅|string|Google Books の書籍ID|

**レスポンス**

json

```json
{
  "id": "xxxxxx",
  "title": "本のタイトル",
  "authors": ["著者名"],
  "thumbnail": "https://...",
  "published_date": "2024-01-01",
  "description": "概要テキスト",
  "page_count": 300,
  "categories": ["技術書"],
  "publisher": "出版社名",
  "isbn": "978-xxxxxxxxxx"
}
```

---

### Google Books API フィールドマッピング

| api-hub フィールド | Google Books API のパス | 備考 |
|---|---|---|
| `id` | `id` | |
| `title` | `volumeInfo.title` | |
| `authors` | `volumeInfo.authors` | 配列 |
| `thumbnail` | `volumeInfo.imageLinks.thumbnail` | smallThumbnail は使わない |
| `published_date` | `volumeInfo.publishedDate` | |
| `description` | `volumeInfo.description` | |
| `page_count` | `volumeInfo.pageCount` | 詳細のみ |
| `categories` | `volumeInfo.categories` | 詳細のみ。配列 |
| `publisher` | `volumeInfo.publisher` | 詳細のみ |
| `isbn` | `volumeInfo.industryIdentifiers` | 詳細のみ。ISBN_13 優先、なければ ISBN_10 |

**フィールドが存在しない場合は `null` を返す。**

---

### エラーレスポンス（共通）

|ステータスコード|内容|
|---|---|
|`400`|リクエストが不正（`q`が空など）|
|`404`|書籍が見つからない|
|`500`|サーバエラー・外部APIエラー|

**エラーレスポンス形式**

json

```json
{
  "error": {
  "code": "NOT_FOUND",
  "message": "書籍が見つかりませんでした"
  }
}
```