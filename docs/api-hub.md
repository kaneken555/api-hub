## api-hub 概要

### 目的

Google Books APIへのリクエストを中継・加工して返す共通APIサーバ

### 当面のスコープ（MVP）

```
クライアント（スマホ/Web）
        ↓
    api-hub
    └── Google Books APIへリクエスト
    └── レスポンスを加工して返す
        ↓
  Google Books API
```

### エンドポイント（例）

|メソッド|パス|内容|
|---|---|---|
|`GET`|`/books/search?q=タイトル`|本を検索|
|`GET`|`/books/:id`|本の詳細取得|

### レスポンスの加工

- Google Books APIの大量フィールドから必要なものだけ返す
- 例：`id`, `title`, `author`, `thumbnail`, `description` など

### 将来の拡張

- 映画APIなど他の外部APIを追加
- 個別バックエンドからのリクエストも受け付ける
- レート制限・認証の追加