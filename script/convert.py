#!/usr/bin/env python3
"""
Simple Markdown to HTML converter wrapper
Usage: python3 convert.py <markdown_file>
"""
import os
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("使用方法: python3 convert.py <markdown_file>")
        print("例: python3 convert.py blog_md/my_article.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    # Check if markdown file exists
    if not os.path.exists(md_file):
        print(f"エラー: ファイル '{md_file}' が見つかりません")
        sys.exit(1)
    
    # Get file info
    md_path = Path(md_file)
    filename = md_path.stem  # filename without extension
    
    # Set default paths (adjust for script directory)
    template_file = "template/template.html"
    output_file = f"../docs/blog_html/{filename}.html"
    blog_index_file = "../docs/blog_index.html"
    
    # Check if template exists
    if not os.path.exists(template_file):
        print(f"エラー: テンプレートファイル '{template_file}' が見つかりません")
        sys.exit(1)
    
    # Check if blog_index exists
    if not os.path.exists(blog_index_file):
        print(f"エラー: ブログインデックスファイル '{blog_index_file}' が見つかりません")
        sys.exit(1)
    
    # Run the conversion
    import subprocess
    
    # Adjust md_file path if it's relative to project root
    if not os.path.isabs(md_file) and not md_file.startswith('../'):
        md_file = f"../{md_file}"
    
    cmd = [
        "python3", "convert_md_to_html.py",
        "--md_file", md_file,
        "--template_file", template_file,
        "--output_file", output_file,
        "--blog_index_file", blog_index_file
    ]
    
    print(f"変換中: {md_file} -> {output_file}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"変換完了: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"エラー: 変換に失敗しました")
        print(f"エラー出力: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("エラー: python3 または convert_md_to_html.py が見つかりません")
        sys.exit(1)


if __name__ == "__main__":
    main()
