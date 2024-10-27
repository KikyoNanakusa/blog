import markdown
from datetime import datetime
import os


def load_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_template(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_date_from_html(html_file):
    if not os.path.exists(html_file):
        return None

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    start_tag = "投稿日: "
    start_idx = html_content.find(start_tag)
    if start_idx == -1:
        return None

    start_idx += len(start_tag)
    end_idx = html_content.find("</p>", start_idx)

    if end_idx == -1:
        return None

    return html_content[start_idx:end_idx].strip()


def generate_html_template(template, title, content, existing_date=None):
    date = (
        existing_date
        if existing_date
        else datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    )
    updated = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

    filled_template = template.replace("{title}", title)
    filled_template = filled_template.replace("{date}", date)
    filled_template = filled_template.replace("{updated}", updated)
    filled_template = filled_template.replace("{content}", content)

    return filled_template


def convert_md_to_html(md_text):
    content = "\n".join(md_text.splitlines()[1:])
    return markdown.markdown(content, extensions=["fenced_code", "tables"])


def save_html_file(file_path, html_content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def update_blog_index(title, html_filename, blog_index_path):
    with open(blog_index_path, "r", encoding="utf-8") as f:
        blog_index_content = f.read()

    if html_filename in blog_index_content:
        print(f"'{html_filename}' というHTMLファイルは既に存在します。追記しません。")
        return

    date = datetime.now().strftime("%Y年%m月%d日")
    name = html_filename.replace("docs/", "")
    new_entry = f'<li><a href="{name}">{title}</a>: {date}</li>'

    updated_content = blog_index_content.replace("<ul>", f"<ul>\n          {new_entry}")

    with open(blog_index_path, "w", encoding="utf-8") as f:
        f.write(updated_content)


def main(md_file, template_file, output_file, blog_index_file):
    md_content = load_markdown_file(md_file)
    template_content = load_template(template_file)
    existing_date = extract_date_from_html(output_file)
    html_content = convert_md_to_html(md_content)
    title = md_content.splitlines()[0].replace("# ", "")
    full_html = generate_html_template(
        template_content, title, html_content, existing_date
    )

    save_html_file(output_file, full_html)
    update_blog_index(title, output_file, blog_index_file)

    print(f"変換が完了しました: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Markdown to HTML and update blog index"
    )
    parser.add_argument("--md_file", required=True, help="Markdown file to convert")
    parser.add_argument("--template_file", required=True, help="HTML template file")
    parser.add_argument("--output_file", required=True, help="Output HTML file")
    parser.add_argument(
        "--blog_index_file", required=True, help="Path to blog_index.html file"
    )

    args = parser.parse_args()
    main(args.md_file, args.template_file, args.output_file, args.blog_index_file)
