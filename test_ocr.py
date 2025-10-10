from paddleocr import PaddleOCR

ocr = PaddleOCR(use_textline_orientation=True, lang='ch')

# 测试一张图片
result = ocr.predict('photo_jpg/IMG_7781.jpg')

print("结果类型:", type(result))
print("结果长度:", len(result))

if result:
    print("\n第一个元素类型:", type(result[0]))
    if isinstance(result[0], dict):
        print("字典的键:", result[0].keys())
        for key, value in result[0].items():
            print(f"\n{key}:")
            if isinstance(value, list) and value:
                print(f"  类型: list, 长度: {len(value)}")
                print(f"  第一个元素: {value[0]}")
            else:
                print(f"  {value}")
