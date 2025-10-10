#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
处理手写读书摘抄图片
- 使用PaddleOCR识别手写内容
- 提取书名信息
- 按书名合并内容
- 输出到final/目录
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from paddleocr import PaddleOCR
import re

# 初始化PaddleOCR（使用中文识别）
ocr = PaddleOCR(use_textline_orientation=True, lang='ch')

# 配置
PHOTO_DIR = "photo_jpg"
OUTPUT_DIR = "final"
SKIP_FILES = ["IMG_7801.jpg"]
START_NUM = 7781
END_NUM = 7817

# 存储所有识别结果
all_results = {}

def ocr_image(image_path):
    """对单张图片进行OCR识别"""
    try:
        result = ocr.predict(str(image_path))
        if result and isinstance(result, list) and len(result) > 0:
            # 提取所有识别的文字
            if 'rec_texts' in result[0]:
                texts = result[0]['rec_texts']
                full_text = '\n'.join(texts) if isinstance(texts, list) else str(texts)
                return full_text
        return ""
    except Exception as e:
        print(f"处理 {image_path} 时出错: {e}")
        return ""

def extract_book_name(text, img_name):
    """从文本中提取书名"""
    # 常见书名模式
    patterns = [
        r'[《〈](.*?)[》〉]',  # 书名号
        r'(红楼梦|月亮与六便士|围城|.*?集)',  # 已知书名
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]

    # 如果没有找到书名，返回None
    return None

def process_all_images():
    """处理所有图片"""
    print("开始处理图片...")

    for num in range(START_NUM, END_NUM + 1):
        filename = f"IMG_{num}.jpg"

        # 跳过指定文件
        if filename in SKIP_FILES:
            print(f"跳过 {filename}")
            continue

        filepath = Path(PHOTO_DIR) / filename

        if not filepath.exists():
            print(f"文件不存在: {filepath}")
            continue

        print(f"正在处理: {filename}")

        # OCR识别
        text = ocr_image(filepath)

        if text:
            all_results[filename] = {
                'text': text,
                'book_name': extract_book_name(text, filename)
            }
            print(f"  识别完成，文本长度: {len(text)}")
            if all_results[filename]['book_name']:
                print(f"  书名: {all_results[filename]['book_name']}")
        else:
            print(f"  未能识别文字")

    # 保存中间结果
    with open('ocr_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n总共处理了 {len(all_results)} 张图片")
    print("OCR结果已保存到 ocr_results.json")

def group_by_book():
    """按书名分组"""
    grouped = defaultdict(list)
    unknown_count = 1

    for filename, data in all_results.items():
        book_name = data['book_name']

        if not book_name:
            book_name = f"未知书籍_{unknown_count}"
            unknown_count += 1

        grouped[book_name].append({
            'filename': filename,
            'text': data['text']
        })

    return grouped

def save_markdown_files(grouped):
    """保存为Markdown文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for book_name, items in grouped.items():
        # 清理文件名中的特殊字符
        safe_filename = re.sub(r'[<>:"/\\|?*《》]', '', book_name)
        md_filename = f"{safe_filename}.md"
        md_path = Path(OUTPUT_DIR) / md_filename

        # 生成Markdown内容
        content = f"# {book_name}\n\n"

        for item in items:
            content += item['text'] + "\n\n"

        # 保存文件
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"已生成: {md_filename} (包含 {len(items)} 张图片)")

if __name__ == "__main__":
    # 第一步：OCR识别所有图片
    process_all_images()

    # 第二步：按书名分组
    print("\n按书名分组...")
    grouped = group_by_book()

    # 第三步：生成Markdown文件
    print("\n生成Markdown文件...")
    save_markdown_files(grouped)

    print("\n处理完成！")
    print(f"共识别出 {len(grouped)} 本书")
    print("书名列表：")
    for book_name in grouped.keys():
        print(f"  - {book_name}")
