import json
import random

def count_jsonl_objects_in_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return sum(1 for line in file)
    except FileNotFoundError:
        print("Error: 文件未找到。")
        return 0



def count_json_objects_in_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return len(data)  # 数组中的元素数量
            else:
                return 1  # 文件包含单个JSON对象
    except json.JSONDecodeError:
        print("Error: 文件不是有效的JSON格式。")
        return 0
    except FileNotFoundError:
        print("Error: 文件未找到。")
        return 0



def shuffle_json_file(input_file_name, output_file_name):
    # 读取 JSON 数据
    with open(input_file_name, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # 打乱 JSON 对象的顺序
    random.shuffle(json_data)

    # 保存打乱顺序后的 JSON 数据
    with open(output_file_name, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def get_json_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data
def save_to_json_file(json_data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def merge_and_save_json_files(file1_path, file2_path, output_file_path):
    # 读取第一个 JSON 文件
    with open(file1_path, 'r', encoding='utf-8') as file:
        data1 = json.load(file)

    # 读取第二个 JSON 文件
    with open(file2_path, 'r', encoding='utf-8') as file:
        data2 = json.load(file)

    # 合并数据
    merged_data = data1 + data2

    # 保存合并后的数据到新的 JSON 文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

    return merged_data

# 示例使用
# jsonl_file_name = 'your_file.jsonl'
# print(f"文件'{jsonl_file_name}'中包含的JSON对象数量：{count_jsonl_objects_in_file(jsonl_file_name)}")

# 示例使用
file_name = '../dataset/llm_conversation_dataset_merge_random_v1.json'
# llm_conversation_dataset_merge_random_v1.json'中包含的JSON对象数量：40468
print(f"文件'{file_name}'中包含的JSON对象数量：{count_json_objects_in_file(file_name)}")