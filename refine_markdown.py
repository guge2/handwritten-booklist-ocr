#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
优化Markdown文件：
1. 纠正明显的书名OCR错误
2. 合并同一本书的内容
3. 清理OCR噪音
4. 调整格式（去掉书名号，清理无用内容）
"""

import os
import re
from pathlib import Path
import json

FINAL_DIR = "final"

# 书名纠正映射
BOOK_NAME_CORRECTIONS = {
    "江楼梦": "红楼梦",
    "话着": "活着",
    "富爸爸穷龟爸": "富爸爸穷爸爸",
    "汉谈拉比法典": "汉谟拉比法典",
    "瓦尔登湖": "瓦尔登湖",
    "Ų威的森林": "挪威的森林",
    "孽子": "孽子",
}

# OCR噪音模式
NOISE_PATTERNS = [
    r'^DATE\s*$',
    r'^OM\s*$',
    r'^OT\s*$',
    r'^oW\s*$',
    r'^So\s*$',
    r'^os\s*$',
    r'^OF\s*$',
    r'^NOTES\s*$',
    r'^front\s*$',
    r'^成分\s*$',
    r'^虚伪牧\s*$',
]

def clean_text(text):
    """清理文本中的OCR噪音"""
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # 跳过空行
        if not line.strip():
            cleaned_lines.append('')
            continue

        # 检查是否是噪音行
        is_noise = False
        for pattern in NOISE_PATTERNS:
            if re.match(pattern, line.strip()):
                is_noise = True
                break

        if not is_noise:
            # 移除行内的书名号《》
            line = re.sub(r'[《》]', '', line)
            cleaned_lines.append(line)

    # 合并连续的空行
    result = []
    prev_empty = False
    for line in cleaned_lines:
        if not line.strip():
            if not prev_empty:
                result.append('')
                prev_empty = True
        else:
            result.append(line)
            prev_empty = False

    return '\n'.join(result)

def merge_books():
    """合并同一本书的内容"""
    # 读取所有MD文件
    files = list(Path(FINAL_DIR).glob('*.md'))
    book_contents = {}

    for filepath in files:
        book_name = filepath.stem

        # 应用书名纠正
        corrected_name = BOOK_NAME_CORRECTIONS.get(book_name, book_name)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取正文（跳过第一行的标题）
        lines = content.split('\n', 1)
        if len(lines) > 1:
            body = lines[1].strip()
        else:
            body = ""

        # 合并内容
        if corrected_name in book_contents:
            book_contents[corrected_name] += '\n\n' + body
        else:
            book_contents[corrected_name] = body

    return book_contents

def save_cleaned_files(book_contents):
    """保存清理后的文件"""
    # 清空final目录
    for file in Path(FINAL_DIR).glob('*.md'):
        file.unlink()

    for book_name, content in book_contents.items():
        # 清理内容
        cleaned_content = clean_text(content)

        # 生成最终内容
        final_content = f"# {book_name}\n\n{cleaned_content}\n"

        # 保存文件
        safe_filename = re.sub(r'[<>:"/\\|?*]', '', book_name)
        filepath = Path(FINAL_DIR) / f"{safe_filename}.md"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"已保存: {safe_filename}.md")

if __name__ == "__main__":
    print("开始优化Markdown文件...")

    # 合并书籍
    print("\n合并同一本书的内容...")
    book_contents = merge_books()

    print(f"\n共有 {len(book_contents)} 本书")

    # 保存清理后的文件
    print("\n保存清理后的文件...")
    save_cleaned_files(book_contents)

    print("\n优化完成！")
    print("\n书籍列表:")
    for book_name in sorted(book_contents.keys()):
        print(f"  - {book_name}")
