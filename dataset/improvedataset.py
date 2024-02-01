import re
import json
from script.file_opration import save_to_json_file
def is_picture_question(json_object):
    # 检查 'question' 属性中是否包含 ![任意字符] 的模式
    return bool(re.search(r'!\[.*?\]', json_object.get("question", "")))

def improve_explanation(explanation):
    improved_results = []
    if explanation=="":
        return []
    for text in explanation:
        # 删除每个字符串元素中第一个满足 r'.{2}：' 格式的部分内容
        text = re.sub(r'^.{2}：', '', text)
        text = re.sub(r'本题主要考察.+?。', '', text)
        text=re.sub(r'相关内容拓展：','',text)
        text = re.sub(r'相关法规参考：', '根据', text)
        new_text=re.sub(r'因此选择.+?。', '', text)
        # 新增代码，删除含有"选项"二字的元素
        if "选项" not in text:
            improved_results.append(new_text)
    return improved_results

# 读取 JSON 数据
file_name = 'structqa_raw.json'
with open(file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

picture_json_list=[]
text_json_list=[]
for item in json_data:
    question=item.get("question", "")
    choose=item.get("choose", "")
    answer=item.get("answer", "")
    explanation=item.get("explanation", [])

    item["explanation"] = improve_explanation(explanation)

    if is_picture_question(item):
        picture_json_list.append(item)
        #print(question)
    else:
        text_json_list.append(item)


print(f"picture_json_list length is {len(picture_json_list)}")
print(f"text_json_list length is {len(text_json_list)}")

# 保存到文件（图片数据集）
save_to_json_file(picture_json_list, 'structqa_picture.json')
# 保存到文件（文本数据集）
save_to_json_file(text_json_list, 'structqa_text.json')
