#!/usr/bin/env python3
"""
Markdown to HTML converter using only standard library
"""
import re
import os
from datetime import datetime
from pathlib import Path


class MarkdownConverter:
    """Markdown to HTML converter using regex patterns"""
    
    def __init__(self):
        self.patterns = [
            # Headers
            (r'^### (.*)$', r'<h3>\1</h3>'),
            (r'^## (.*)$', r'<h2>\1</h2>'),
            (r'^# (.*)$', r'<h1>\1</h1>'),
            
            # Bold and italic
            (r'\*\*(.*?)\*\*', r'<strong>\1</strong>'),
            (r'\*(.*?)\*', r'<em>\1</em>'),
            
            # Code blocks
            (r'```(.*?)```', r'<pre><code>\1</code></pre>', re.DOTALL),
            (r'`(.*?)`', r'<code>\1</code>'),
            
            # Links
            (r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>'),
            
            # Line breaks are handled later by paragraph wrapping
        ]
    
    def convert(self, markdown_text):
        """Convert markdown text to HTML"""
        # Remove first line (title) and process content
        lines = markdown_text.splitlines()
        if lines and lines[0].startswith('#'):
            content_lines = lines[1:]
        else:
            content_lines = lines
        
        # Process line by line with nested list support
        processed_lines = []
        current_depth = 0  # 0 means not inside any list
        li_open = False    # whether a <li> is currently open at current_depth
        current_bq_depth = 0  # 0 means not inside any blockquote

        for raw_line in content_lines:
            if not raw_line.strip():
                # Empty line - close all open structures gracefully
                if li_open:
                    processed_lines.append('</li>')
                    li_open = False
                while current_depth > 0:
                    processed_lines.append('</ul>')
                    current_depth -= 1
                    # when closing a level, also close the parent li if it was awaiting siblings
                    if current_depth > 0:
                        processed_lines.append('</li>')
                # Close any open blockquotes on empty line (simple behavior)
                while current_bq_depth > 0:
                    processed_lines.append('</blockquote>')
                    current_bq_depth -= 1

                processed_lines.append('')  # empty line marker
                continue

            # Detect blockquote lines (one or more leading '>' possibly with spaces)
            m_bq = re.match(r'^(?P<markers>(?:>\s*)+)(.*)$', raw_line)
            if m_bq:
                markers = m_bq.group('markers')
                # Count '>' characters to determine nesting depth
                target_bq = markers.count('>')

                # Adjust blockquote depth (open or close tags as needed)
                if target_bq > current_bq_depth:
                    for _ in range(current_bq_depth, target_bq):
                        processed_lines.append('<blockquote>')
                    current_bq_depth = target_bq
                elif target_bq < current_bq_depth:
                    for _ in range(current_bq_depth - target_bq):
                        processed_lines.append('</blockquote>')
                    current_bq_depth = target_bq

                # Replace raw_line with the inner content after the '>' markers
                raw_line = m_bq.group(2)

            line_stripped = raw_line.strip()

            # Check for headers (operate outside of lists)
            if re.match(r'^### (.*)$', line_stripped):
                if li_open:
                    processed_lines.append('</li>')
                    li_open = False
                while current_depth > 0:
                    processed_lines.append('</ul>')
                    current_depth -= 1
                    if current_depth > 0:
                        processed_lines.append('</li>')
                processed_lines.append(f'<h3>{re.match(r"^### (.*)$", line_stripped).group(1)}</h3>')
                continue
            elif re.match(r'^## (.*)$', line_stripped):
                if li_open:
                    processed_lines.append('</li>')
                    li_open = False
                while current_depth > 0:
                    processed_lines.append('</ul>')
                    current_depth -= 1
                    if current_depth > 0:
                        processed_lines.append('</li>')
                processed_lines.append(f'<h2>{re.match(r"^## (.*)$", line_stripped).group(1)}</h2>')
                continue
            elif re.match(r'^# (.*)$', line_stripped):
                if li_open:
                    processed_lines.append('</li>')
                    li_open = False
                while current_depth > 0:
                    processed_lines.append('</ul>')
                    current_depth -= 1
                    if current_depth > 0:
                        processed_lines.append('</li>')
                processed_lines.append(f'<h1>{re.match(r"^# (.*)$", line_stripped).group(1)}</h1>')
                continue

            # Detect unordered list item with indent (supports -, *, +)
            m = re.match(r'^(\s*)([-*+])\s+(.*)$', raw_line)
            if m:
                indent = m.group(1)
                content_text = m.group(3)
                # tabs count as 4 spaces; one nesting level per 2 spaces
                indent_spaces = len(indent.replace('\t', '    '))
                target_depth = indent_spaces // 2 + 1

                # Adjust depth
                if target_depth > current_depth:
                    # open new <ul> levels (if increasing without an open li at top, it's fine)
                    # when increasing from >=1, keep current <li> open so nested <ul> is inside it
                    for _ in range(current_depth, target_depth):
                        processed_lines.append('<ul>')
                    current_depth = target_depth
                elif target_depth == current_depth:
                    if li_open:
                        processed_lines.append('</li>')
                        li_open = False
                else:  # target_depth < current_depth
                    if li_open:
                        processed_lines.append('</li>')
                        li_open = False
                    # close levels down to target_depth
                    for _ in range(current_depth - target_depth):
                        processed_lines.append('</ul>')
                        # after closing a nested list, we are back inside a parent <li>
                        # that parent <li> should end before starting next sibling
                        processed_lines.append('</li>')
                    current_depth = target_depth

                # Start new list item
                processed_lines.append(f'<li>{content_text}')
                li_open = True
                continue

            # Regular paragraph/text line
            if li_open:
                # Text line after an open <li> indicates continuation of the same list item
                processed_lines.append('<br>' + line_stripped)
                continue

            # Not in list context
            processed_lines.append(line_stripped)

        # Close any remaining open list structures
        if li_open:
            processed_lines.append('</li>')
            li_open = False
        while current_depth > 0:
            processed_lines.append('</ul>')
            current_depth -= 1
            if current_depth > 0:
                processed_lines.append('</li>')
        # Close any remaining open blockquotes
        while current_bq_depth > 0:
            processed_lines.append('</blockquote>')
            current_bq_depth -= 1
        
        content = '\n'.join(processed_lines)
        
        # Process code blocks
        content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)
        
        # Apply other conversion patterns
        for pattern, replacement, *flags in self.patterns:
            if pattern.startswith('```') or pattern.startswith('^#'):  # Skip already processed patterns
                continue
            if flags:
                content = re.sub(pattern, replacement, content, flags=flags[0])
            else:
                content = re.sub(pattern, replacement, content)
        
        # Clean up br tags around lists
        content = re.sub(r'<br>\s*<ul>', '<ul>', content)
        content = re.sub(r'</ul>\s*<br>', '</ul>', content)
        content = re.sub(r'<br>\s*<li>', '<li>', content)
        content = re.sub(r'</li>\s*<br>', '</li>', content)
        content = re.sub(r'</li>\s*<ul>', '<ul>', content)
        
        # Process content preserving empty lines
        lines = content.split('\n')
        wrapped_paragraphs = []
        current_para = []

        for line in lines:
            # Handle special elements (don't strip these)
            if (line.startswith('<pre><code>') and line.endswith('</code></pre>')) or \
               line.startswith('<h') or line.startswith('<ul>') or line.startswith('<li>') or line.startswith('</ul>') or line.startswith('</li>') or line.startswith('<blockquote>') or line.startswith('</blockquote>'):
                # Flush current paragraph if any
                if current_para:
                    para_text = '\n'.join(current_para)
                    para_text = re.sub(r'\n', '<br>', para_text)
                    wrapped_paragraphs.append(f'<p>{para_text}</p>')
                    current_para = []

                # Add special element
                wrapped_paragraphs.append(line)
            elif not line.strip():
                # Empty line - flush current paragraph but don't add br
                if current_para:
                    para_text = '\n'.join(current_para)
                    para_text = re.sub(r'\n', '<br>', para_text)
                    wrapped_paragraphs.append(f'<p>{para_text}</p>')
                    current_para = []
                # Don't add <br> for empty lines - let CSS handle spacing
            else:
                # Regular line - add to current paragraph
                current_para.append(line.strip())

        # Flush remaining paragraph
        if current_para:
            para_text = '\n'.join(current_para)
            para_text = re.sub(r'\n', '<br>', para_text)
            wrapped_paragraphs.append(f'<p>{para_text}</p>')

        # Join all elements
        return '\n'.join(wrapped_paragraphs)
    


def load_file(file_path):
    """Load file content with error handling"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません")
        return None
    except Exception as e:
        print(f"エラー: ファイル '{file_path}' の読み込みに失敗しました: {e}")
        return None


def save_file(file_path, content):
    """Save content to file with error handling"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"エラー: ファイル '{file_path}' の保存に失敗しました: {e}")
        return False


def extract_date_from_html(html_file):
    """Extract existing date from HTML file"""
    if not os.path.exists(html_file):
        return None
    
    content = load_file(html_file)
    if not content:
        return None
    
    # Look for date pattern
    date_pattern = r'投稿日: ([^<]+)'
    match = re.search(date_pattern, content)
    
    return match.group(1).strip() if match else None


def generate_html_template(template, title, content, existing_date=None):
    """Generate HTML from template"""
    date = (
        existing_date
        if existing_date
        else datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    )
    updated = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    
    return template.replace("{title}", title).replace("{date}", date).replace("{updated}", updated).replace("{content}", content)


def update_blog_index(title, html_filename, blog_index_path):
    """Update blog index with new entry or update existing entry"""
    content = load_file(blog_index_path)
    if not content:
        return False
    
    # Extract filename for comparison
    filename = html_filename.replace("docs/", "")
    filename = filename.replace("../", "")
    
    # Check if entry already exists by looking for the href pattern
    href_pattern = rf'<a href="{re.escape(filename)}">'
    existing_match = re.search(href_pattern, content)
    
    if existing_match:
        # Update existing entry with new date
        date = datetime.now().strftime("%Y年%m月%d日")
        # Find the entire <li> tag and replace it
        li_pattern = rf'<li><a href="{re.escape(filename)}">[^<]*</a>: [^<]*</li>'
        new_entry = f'<li><a href="{filename}">{title}</a>: {date}</li>'
        updated_content = re.sub(li_pattern, new_entry, content)
        print(f"'{filename}' のエントリを更新しました")
        return save_file(blog_index_path, updated_content)
    
    # Also check if the same title already exists with different filename
    title_pattern = rf'<li><a href="[^"]*">{re.escape(title)}</a>: [^<]*</li>'
    if re.search(title_pattern, content):
        print(f"タイトル '{title}' は既にインデックスに存在します（異なるファイル名）")
        return True
    
    # Generate new entry
    date = datetime.now().strftime("%Y年%m月%d日")
    new_entry = f'<li><a href="{filename}">{title}</a>: {date}</li>'
    
    # Insert new entry at the beginning of the list (newest first)
    updated_content = content.replace("<ul>", f"<ul>\n          {new_entry}")
    
    return save_file(blog_index_path, updated_content)


def main(md_file, template_file, output_file, blog_index_file):
    """Main conversion function"""
    print(f"Markdownファイルを変換中: {md_file}")
    
    # Load files
    md_content = load_file(md_file)
    template_content = load_file(template_file)
    
    if not md_content or not template_content:
        print("必要なファイルの読み込みに失敗しました")
        return False
    
    # Extract title and convert content
    lines = md_content.splitlines()
    title = lines[0].replace("# ", "") if lines and lines[0].startswith("#") else "Untitled"
    
    converter = MarkdownConverter()
    html_content = converter.convert(md_content)
    
    # Get existing date if file exists
    existing_date = extract_date_from_html(output_file)
    
    # Generate final HTML
    full_html = generate_html_template(template_content, title, html_content, existing_date)
    
    # Save HTML file
    if not save_file(output_file, full_html):
        return False
    
    # Update blog index
    if not update_blog_index(title, output_file, blog_index_file):
        print("警告: ブログインデックスの更新に失敗しました")
    
    print(f"変換完了: {output_file}")
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MarkdownをHTMLに変換し、ブログインデックスを更新します"
    )
    parser.add_argument("--md_file", required=True, help="変換するMarkdownファイル")
    parser.add_argument("--template_file", required=True, help="HTMLテンプレートファイル")
    parser.add_argument("--output_file", required=True, help="出力HTMLファイル")
    parser.add_argument("--blog_index_file", required=True, help="blog_index.htmlファイルのパス")
    
    args = parser.parse_args()
    
    success = main(args.md_file, args.template_file, args.output_file, args.blog_index_file)
    exit(0 if success else 1)