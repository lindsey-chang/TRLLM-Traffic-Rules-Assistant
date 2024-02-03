# 数据集制作笔记

## RAG数据集

>**[通过Google Drive访问我们的进行RAG的原始数据与处理后的数据](https://drive.google.com/drive/folders/1byb6ygquCQe9joAHZayYF1SUat3q8lKN?usp=sharing)**

### 原始数据
1. 搜集了公安部令与国务院令中有关机动车驾驶、道路交通规则等一系列法规条令。
2. 搜集了驾驶证考试科目一、科目二、科目三、科目四有关的考试技巧口诀
3. 使用开源项目[Bili2text](https://github.com/lanbinshijie/bili2text)，将B站中科目二、科目三的驾考培训视频转为文本数据。

![rag_raw_data.png](../assets/rag_raw_data.png)


### 处理原始数据 
手工整理、整合数据，将所有数据统一为`txt`格式。

## 微调数据集

>**[通过Google Drive访问我们微调阶段的数据集](https://drive.google.com/drive/folders/1g0N1qDH0WYPYmCthUZdDtVSolfOKo-UH?usp=sharing)**

### 原始数据
网络上搜集的驾考科目一、科目四选择题题库。其中有一部分题库只有选项答案没有解析，另部分有答案解析。

为了在进行指令跟随微调后，TRLLM模型能针对用户的提问，不仅要给出正确的回答，还需要给出详细的解释。因此我们将有解析的科目一科目四题库制作为用作**指令跟随微调的数据集**，而只有答案没有解析的科目一科目四题库我们将其制作为**评测数据集**用来评测微调和量化后TRLLM的性能。

- 没有解析的科目一题库：共1853条选择题。
- 没有解析的科目四题库：共1590条选择题。
- 有解析的科目一题库：共1615条选择题。
- 有解析的科目四题库：共1383条选择题。

上述题库中，其中有部分看图答题的题目，在后续制作文本数据集时进行了过滤，因此有一定的数据损失。

### 处理原始数据


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

## 评测数据集