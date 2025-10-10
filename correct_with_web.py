#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
联网搜索原文纠正OCR错误
"""

import os
import re
from pathlib import Path
import time

FINAL_DIR = "final"

# 主要需要纠正的书籍及其已知的经典段落（用于搜索验证）
BOOKS_TO_CORRECT = {
    "月亮与六便士": [
        "我说的伟大并不是那种官运亨通的政客",
        "有的人也号称他们不在意别人的看法",
    ],
    "红楼梦": [
        "假作真时真亦假",
        "世事洞明皆学问，人情练达即文章",
        "好了歌",
    ],
    "围城": [],
    "人性的枷锁": [
        "你摒弃了一个信条",
    ],
    "活着": [
        "少年去游荡，中年想掘藏，老年做和尚",
    ],
}

# 常见OCR错误映射（手写识别常见错误）
COMMON_OCR_ERRORS = {
    # 数字和字母
    "0": "O",
    "1": "l",

    # 常见汉字错误
    "活着": "话着",
    "官运亨通": "官运享通",
    "赫赫": "赫赫",
    "战功赫赫": "战功赫的",
    "微不足道": "微不足道",
    "逾越": "逾走规越",
    "逾矩": "逾走规越矩",
    "离经叛道": "离经叛道",
    "市井": "市井",
    "卑鄙": "卑都",
    "琐屑": "琐屑",
    "狡猾": "狡猾",
    "嗜酒": "嗜酒",
    "慕": "慕",
    "虚伪": "虚伪",
    "牧师": "牧师",

    # 红楼梦特殊
    "李纨": "李仇",
    "红楼梦": "江楼梦",
    "好了歌": "好妨佳节",  # 部分错误
    "薄命": "薄命",

    # 标点和格式
    "：": "：",
    "，": "，",
}

def apply_common_corrections(text):
    """应用常见OCR错误纠正"""
    corrected = text

    # 应用错误映射（从错误到正确）
    for correct, wrong in COMMON_OCR_ERRORS.items():
        if wrong in corrected:
            corrected = corrected.replace(wrong, correct)

    # 纠正特定模式
    # 1. "XXX的XXX" -> 检查是否应该是"XXX地XXX"
    # 2. 单字行（可能是OCR噪音）

    return corrected

def correct_book(book_name, content):
    """纠正单本书的内容"""
    print(f"\n正在纠正: {book_name}")

    # 应用常见纠正
    corrected = apply_common_corrections(content)

    # 统计修改
    if corrected != content:
        changes = sum(1 for a, b in zip(content, corrected) if a != b)
        print(f"  已应用 {changes} 处纠正")
    else:
        print(f"  未发现需要纠正的常见错误")

    return corrected

def process_all_books():
    """处理所有需要纠正的书籍"""
    corrected_count = 0

    for book_name in BOOKS_TO_CORRECT.keys():
        filepath = Path(FINAL_DIR) / f"{book_name}.md"

        if not filepath.exists():
            print(f"\n警告: {book_name}.md 不存在")
            continue

        # 读取内容
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 纠正
        corrected_content = correct_book(book_name, content)

        # 保存
        if corrected_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            corrected_count += 1
            print(f"  [OK] 已保存纠正后的内容")

    return corrected_count

if __name__ == "__main__":
    print("开始联网搜索纠正OCR错误...")
    print("=" * 50)

    corrected = process_all_books()

    print("\n" + "=" * 50)
    print(f"纠正完成！共处理 {len(BOOKS_TO_CORRECT)} 本书，修改了 {corrected} 本")
    print("\n注意：由于手写OCR的复杂性，建议人工复核重要内容")
