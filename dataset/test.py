import re

# 示例文本
text = """【技巧 1】爆胎导致事故，超载属于隐患。\n\n【技巧 2】解析：车辆上路行驶前应检查车辆安全性能，避免突发爆胎导致发生事 故。 
\n\n【讲解 1】本题主要考察安全驾驶常识。车辆爆胎影响驾驶安全，导致发生本次事 故。因此选择“正确”。 \n\n【讲解 2】相关法规参考：《道路交通安全法》第二十一条，驾驶人驾驶机动车上 
道路行驶前，应当对机动车的安全技术性能进行认真检查；不得驾驶安全设施不 
全或者机件不符合技术标准等具有安全隐患的机动车。"""

# 使用正则表达式提取特定内容
# 提取每个在 "】" 和 "【" 之间的文本
extracted_contents1 = re.findall(r'】(.*?)【', text, re.DOTALL)
extracted_contents2 = re.findall(r'】([^】]*)$', text,re.DOTALL)
extracted_contents1.append(extracted_contents2[0])
print(extracted_contents1)