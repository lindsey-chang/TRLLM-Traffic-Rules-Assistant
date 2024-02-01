import re
import json
from script.file_opration import save_to_json_file

def extract_question_text(text):
    # 使用正则表达式匹配所需文本
    match = re.search(r'\d+、(.+?)A、', text)
    if match:
        # 过滤掉所有空格和换行符，并返回匹配到的文本
        filtered_text = match.group(1).replace(" ", "").replace("\\n", "")
        return filtered_text.strip()
    return ""


def extract_choose_text(text):
    # 使用正则表达式匹配所需文本
    match = re.search(r'\d+、.*?(A、.+?)\\n\\n【答案】', text, re.DOTALL)
    if match:
        # 返回匹配到的文本
        return match.group(1).strip()
    return ""


def extract_answer_text(text):
    # 使用正则表达式匹配所需文本
    match = re.search(r'【答案】(.*?)【', text, re.DOTALL)
    if match:
        # 返回匹配到的文本
        text = match.group(1).replace(" ", "").replace("\\n", "")
        filtered_text = re.sub(r'[^A-Za-z]', '', text)
        return filtered_text.strip()
    return ""


def extract_explaination_list(text):
    # 使用正则表达式匹配所需文本
    match = re.search(r'【答案】.*?【(.*?)$', text)
    if match:
        # 过滤掉所有空格和换行符，并返回匹配到的文本
        text = "【" + match.group(1).strip().replace(" ", "").replace("\\n", "")
        contents1 = re.findall(r'】(.*?)【', text, re.DOTALL)
        contents2 = re.findall(r'】([^】]*)$', text, re.DOTALL)
        contents1.append(contents2[0])
        return contents1
    return ""




def create_json_object(question, choose, answer, explanation):
    """
    创建包含问题、选项、答案和解释的 JSON 对象。

    :param question: 问题文本
    :param choose: 选项文本
    :param answer: 答案文本
    :param explanation: 解释文本
    :return: 构造的 JSON 对象
    """
    return {
        "question": question,
        "choose": choose,
        "answer": answer,
        "explanation": explanation
    }





# 读取 JSON 数据
file_name = 'rawtext.json'
with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

struct_json_data=[]

# 假设您已经从 JSON 文件中加载了数据到变量 json_data
for item in json_data:
    text = str(item["text"])
    extracted_text_question = extract_question_text(text)
    extracted_text_choose = extract_choose_text(text)
    extracted_text_answer = extract_answer_text(text)
    extracted_text_explanation = extract_explaination_list(text)
    # print(extracted_text_question + "\n" + extracted_text_choose + "\n" + extracted_text_answer + "\n"+str(extracted_text_explanation)+"\n---")
    json_object = create_json_object(extracted_text_question, extracted_text_choose, extracted_text_answer,
                                     extracted_text_explanation)
    struct_json_data.append(json_object)
    print(json_object)

# 保存到文件（原始数据集）
save_to_json_file(struct_json_data, 'structqa_raw.json')