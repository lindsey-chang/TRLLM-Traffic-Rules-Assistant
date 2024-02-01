"""
生成internML大模型训练所需的dataset格式
"""
import json






# 读取 JSON 数据
file_name = 'structqa_text.json'
with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)


for item in json_data:
    question=item.get("question", "")
    choose=item.get("choose", "")
    answer=item.get("answer", "")
    explanation=item.get("explanation", "")


