# 数据集制作笔记

## RAG数据集

### 原始数据
1. 搜集了公安部令与国务院令中有关机动车驾驶、道路交通规则等一系列法规条令。
2. 搜集了驾驶证考试科目一、科目二、科目三、科目四有关的考试技巧口诀
3. 使用开源项目[Bili2text](https://github.com/lanbinshijie/bili2text)，将B站中科目二、科目三的驾考培训视频转为文本数据。

![rag_raw_data.png](../assets/rag_raw_data.png)

**[通过Google Drive访问我们的原始数据](https://drive.google.com/drive/folders/1byb6ygquCQe9joAHZayYF1SUat3q8lKN?usp=sharing)**


### 处理原始数据 
（小标题可更改为你觉得更合适的）

## 微调数据集


picture_json_list length is 1352
text_json_list length is 1646

8230
7980
33834

```
llm_json_structure = llm_json_structure * 5  # 因原始数据集条数太少，故将数据集扩充10倍(v1-new版本改为扩展5倍，因为我们有了基于文心一言优化用词的v3)
print(len(llm_json_structure))

# 扩充 llm_conversation_dataset_v3.json 数据集 5 倍
v3_expanded_data = read_and_expand_json_file('./json/finetune_json/llm_conversation_dataset_v3.json', 5)

# 保存扩充后的数据集
v3_expanded_file_path = './json/finetune_json/llm_conversation_dataset_v3_expanded.json'
print(len(v3_expanded_data))

save_json_to_file(v3_expanded_data, v3_expanded_file_path)

file_name = './json/finetune_json/llm_conversation_dataset_merge_new.json'
json_data_m = get_json_from_file(file_name)
print(len(json_data_m))
```