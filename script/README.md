# Scripts

このディレクトリにはブログ管理用のスクリプトが含まれています。

## convert_md_to_html.py

MarkdownファイルをHTMLに変換し、ブログインデックスを自動更新するスクリプトです。

### 機能

- MarkdownファイルをHTMLに変換
- 既存のHTMLファイルから投稿日を保持
- ブログインデックスへの自動追加
- 標準ライブラリのみで動作（外部依存なし）

### 使用方法

```bash
python3 script/convert_md_to_html.py \
  --md_file blog_md/記事名.md \
  --template_file script/template/template.html \
  --output_file docs/blog_html/記事名.html \
  --blog_index_file docs/blog_index.html
```

### パラメータ

- `--md_file`: 変換するMarkdownファイルのパス
- `--template_file`: HTMLテンプレートファイルのパス
- `--output_file`: 出力先HTMLファイルのパス
- `--blog_index_file`: ブログインデックスファイルのパス

### 例

```bash
# 新しい記事を変換
python3 script/convert_md_to_html.py \
  --md_file blog_md/my_article.md \
  --template_file script/template/template.html \
  --output_file docs/blog_html/my_article.html \
  --blog_index_file docs/blog_index.html
```

### 注意事項

- Markdownファイルの最初の行は`# タイトル`の形式である必要があります
- 既存のHTMLファイルがある場合、投稿日は保持されます
- ブログインデックスに同じファイルが既に存在する場合は追加されません
- 出力先ディレクトリが存在しない場合は自動作成されます

### サポートされるMarkdown記法

- 見出し（# ## ###）
- 太字（**text**）
- 斜体（*text*）
- インラインコード（`code`）
- コードブロック（```code```）
- リンク（[text](url)）
- 段落分け（空行）

## template/

HTMLテンプレートファイルが格納されています。

### template.html

ブログ記事用のHTMLテンプレートです。以下のプレースホルダーが使用できます：

- `{title}`: 記事タイトル
- `{date}`: 投稿日
- `{updated}`: 更新日
- `{content}`: 記事内容（HTML）
