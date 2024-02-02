import re
from script.file_opration import *


def contains_keywords(output_text):
    # 定义关键词列表
    keywords = ["改进后", "混乱", "语序", "感谢", "指正", "优化后", "困惑", "改进", "亲和力", "抱歉", "句意", "语序"]
    # 将关键词列表转换为正则表达式模式（用|表示“或”）
    pattern = "|".join(keywords)

    # 搜索output_text中是否包含任意一个关键词
    if re.search(pattern, output_text):
        return True
    else:
        return False


def remove_keywords_section(output_text):
    # 定义关键词列表
    keywords = ["改进后", "混乱", "语序", "感谢", "指正", "优化后", "困惑", "改进", "亲和力", "抱歉", "句意", "语序"]
    # 将关键词列表转换为正则表达式模式（用|表示“或”），匹配除句号外的任意字符，关键词，除句号外的任意字符
    pattern1 = r"[^。]*?(" + "|".join(keywords) + ")[^。]*?\."

    # 使用正则表达式的sub方法删除匹配的部分
    modified_text = re.sub(pattern1, "", output_text)

    # 构建正则表达式：匹配从字符串开头到包含关键词及后面的句号
    pattern2= r"^([^。]*?(" + "|".join(keywords) + ")[^。]*?。)"

    # 使用正则表达式的sub方法删除匹配的部分
    modified_text = re.sub(pattern2, "", modified_text, flags=re.DOTALL)

    return modified_text.strip()


def create_json_object(system, input, output):

    return {
        "system": system,
        "input": input,
        "output": output,
    }

llm_json_structure = []
file_name = '../json/finetune_json/llm_conversation_dataset_v3.json'

with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)


for item in json_data:

    system = item['conversation'][0].get("system", "")
    input = item['conversation'][0].get("input", "")
    output=item['conversation'][0]['output']
    if contains_keywords(output):
        output=remove_keywords_section(output)

    json_object=create_json_object(system, input, output)
    llm_json_structure.append({"conversation": [json_object]})

file_name_n = '../json/finetune_json/llm_conversation_dataset_v3.json'

# 将最终结构保存到原来的 JSON 文件中

with open(file_name_n, 'w', encoding='utf-8') as file:
    json.dump(llm_json_structure, file, ensure_ascii=False, indent=4)

