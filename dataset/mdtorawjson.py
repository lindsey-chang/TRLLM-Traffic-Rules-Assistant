import re
import json
from checkmd import check_question_number

# 原始无格式文本['course1-1-100.md','course1-101-200.md','course1-201-300.md','course1-301-500.md','course1-501-700.md','course1-701-846.md']
file_names = ['./md/course1-1-100.md','./md/course1-101-200.md','./md/course1-201-300.md','./md/course1-301-500.md','./md/course1-501-700.md','./md/course1-701-846.md', './md/course4-1-100.md', './md/course4-101-250.md', './md/course4-251-350.md', './md/course4-351-450.md',
              './md/course4-451-740.md']
raw_text = ""

# 首先匹配所有可能的题号，然后在处理匹配到的字符串时检查它们是否为递增序列。

# 读取并拼接文件内容
for file_name in file_names:
    with open(file_name, 'r', encoding='utf-8') as file:
        raw_text += file.read() + "\n"  # 添加额外的换行符用于分隔不同文件的内容

# 使用正则表达式匹配所有可能的题号
matched_strings = re.findall(r'\n\d+、', raw_text)

# print(matched_strings)
# 检查正则表达式提取出的题号有无遗漏
check_question_number(matched_strings)

# 使用正则表达式分割问题
questions = re.split(r'\n\d+、', raw_text)

# 删除第一个空字符串，因为第一个分割结果通常为空
questions = questions[1:]

# 准备JSON数据结构
json_data = []

for i, question in enumerate(questions, start=1):
    # 替换所有换行符为"\\n"，并移除多余的空格
    formatted_question = question.strip().replace("\n", "\\n")

    # 添加到JSON结构
    json_data.append({
        "no": str(i),
        "text": str(i)+"、"+formatted_question
    })

# 转换为JSON格式的字符串
json_output = json.dumps(json_data, ensure_ascii=False, indent=4)# ensure_ascii=False允许输出字符串包含非 ASCII 字符，比如 Unicode 字符（例如中文、日文、特殊符号等）。
# 将JSON字符串存储到文件
with open('json/raw_json/rawtext.json', 'w', encoding='utf-8') as file:
    file.write(json_output)

print(json_output)
