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
#
# 读取 JSON 数据
file_name = 'structqa_text.json'
with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)


for item in json_data:
    merge_choose_answer_explanation(item)






