import markdown
from datetime import datetime
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="MarkdownをHTMLに変換し、テンプレートに埋め込むスクリプト"
    )
    parser.add_argument("--md_file", help="Markdown path")
    parser.add_argument("--template_file", help="HTML template path")
    parser.add_argument("--output_file", help="Converted html path")
    return parser.parse_args()


def load_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_template(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_html_template(template, title, content):
    date = datetime.now().strftime("%Y年%m月%d日")

    filled_template = template.replace("{title}", title)
    filled_template = filled_template.replace("{date}", date)
    filled_template = filled_template.replace("{content}", content)

    return filled_template


def convert_md_to_html(md_text):
    return markdown.markdown(md_text, extensions=["fenced_code", "tables", "footnotes"])


def save_html_file(file_path, html_content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    args = parse_arguments()

    md_content = load_markdown_file(args.md_file)

    template_content = load_template(args.template_file)

    html_content = convert_md_to_html(md_content)

    title = md_content.splitlines()[0].replace("# ", "")

    full_html = generate_html_template(template_content, title, html_content)

    save_html_file(args.output_file, full_html)

    print(f"[LOG] Complete convertion: {args.output_file}")


if __name__ == "__main__":
    main()
