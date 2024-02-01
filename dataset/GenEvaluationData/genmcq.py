import json, re
from script.file_opration import *
import string




def create_mcq_json_object(question,choose_list,answer):

    # 创建一个空的JSON对象
    json_object = {}
    json_object["question"]=question
    # 获取字母表的前N个字母，N为choose_list的长度
    letters = string.ascii_uppercase[:len(choose_list)]

    # 遍历choose_list，并将每个元素分配给对应的字母属性
    for letter, choice in zip(letters, choose_list):
        json_object[letter] = choice

    json_object["answer"] = answer

    return json_object
def split_choose_text(choose_text):
    # 更新正则表达式以直接匹配任意文本，包括换行符
    patterns = [
        r"(?<=A、)(.*?)(?=B、|$)",
        r"(?<=B、)(.*?)(?=C、|$)",
        r"(?<=C、)(.*?)(?=D、|$)",
        r"(?<=D、)(.*)"
    ]

    # 搜索匹配项并编译结果
    matches = []
    for pattern in patterns:
        match = re.search(pattern, choose_text, re.DOTALL)  # 使用re.DOTALL使.匹配包括换行符在内的任意字符
        if match:
            # 应用strip()和replace()到匹配的字符串，而不是re.Match对象
            match_text = match.group(0).replace("\\n", "").replace("\n","").strip()
            matches.append(match_text)
    return matches

def create_json_object(system, input, output):

    return {
        "system": system,
        "input": input,
        "output": output,
    }

# 读取 JSON 数据
file_name = '../structqa_text.json'
json_data=get_json_from_file(file_name)
# 指定要写入的JSONL文件路径
jsonl_filename = "mcq_data.jsonl"

total_json_number=0
with open(jsonl_filename, 'w', encoding='utf-8') as file:
    for item in json_data:
        question = item.get("question", "")
        choose_text=item.get("choose","")
        answer=item.get("answer","")
        choose_list=split_choose_text(choose_text)
        print(choose_list)

        # 因为未知opencompass是否支持多项选择题，所以过滤掉answer长度大于1的多选题
        if len(answer)==1:
            json_object=create_mcq_json_object(question,choose_list,answer)
            # 将每个元素转换为JSON字符串，并写入文件的单独一行
            json_line = json.dumps(json_object,ensure_ascii=False)
            file.write(json_line + '\n')
            total_json_number+=1

print(f"mcq_data.jsonl has {total_json_number} rows data")


