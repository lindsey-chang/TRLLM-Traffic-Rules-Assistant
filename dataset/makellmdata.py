import json,re
"""
生成internML大模型训练所需的dataset格式
"""

def merge_choose_answer_explanation(json_item):

    choose=json_item.get("choose", "")
    answer=json_item.get("answer", "")
    explanation = json_item.get("explanation", "")
    choiceslist=extract_choiceslist_from_answer(choose,answer)

    # 检查 choiceslist 是否为空
    if not choiceslist:
        print(json_item)
        print("选项列表为空，无法合并。")
        return "选项列表为空，无法合并。"

    merge_text = choiceslist[0].strip()
    if len(choiceslist)>1:
        for i in range(1,len(choiceslist)):
            if i ==len(choiceslist)-1:
                merge_text += "和" + choiceslist[i]
                break
            merge_text+="、"+choiceslist[i]

    merge_text+="。\n因为"
    for exp in explanation:
        merge_text+=exp
    return merge_text




def extract_choiceslist_from_answer(choose, answer):
    # 根据 answer 提取 choose 中对应选项的文本内容
    extracted_choices = []
    for char in answer:
        # 更新正则表达式以更灵活地匹配选择项后面的内容
        match = re.search(rf'{char}、(.*?)(\\n\\n|$)', choose)
        if match:
            extracted_choices.append(match.group(1))
    return extracted_choices

def create_json_object(system, input, output):
    """
    创建包含问题、选项、答案和解释的 JSON 对象。

    :param question: 问题文本
    :param choose: 选项文本
    :param answer: 答案文本
    :param explanation: 解释文本
    :return: 构造的 JSON 对象
    """
    return {
        "system": system,
        "input": input,
        "output": output,
    }


# 创建一个新的 JSON 文件结构用于存储符合模型训练数据集格式的json文件
llm_json_structure = []
# 读取 JSON 数据
file_name = 'structqa_text.json'
with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

system="你现在是一名道路安全规则专家，你需要帮助用户解答各种交通规则问题以及向用户提供驾驶车辆需要了解的各种知识，你需要给出专业、可靠、有逻辑的回答，同时用词还需要具有亲和力。"
for item in json_data:

    input=item.get("question", "")
    output=merge_choose_answer_explanation(item)
    json_object=create_json_object(system,input,output)
    llm_json_structure.append({"conversation": [json_object]})

# 将最终结构保存到新的 JSON 文件中
output_file_name = 'llm_conversation_dataset_v1.json'
with open(output_file_name, 'w', encoding='utf-8') as file:
    json.dump(llm_json_structure, file, ensure_ascii=False, indent=4)






