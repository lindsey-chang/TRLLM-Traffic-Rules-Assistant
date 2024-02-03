# 数据集制作笔记

## RAG数据集

> **[通过Google Drive访问我们的进行RAG的原始数据与处理后的数据](https://drive.google.com/drive/folders/1byb6ygquCQe9joAHZayYF1SUat3q8lKN?usp=sharing)**

### 原始数据

1. 搜集了公安部令与国务院令中有关机动车驾驶、道路交通规则等一系列法规条令。
2. 搜集了驾驶证考试科目一、科目二、科目三、科目四有关的考试技巧口诀
3. 使用开源项目[Bili2text](https://github.com/lanbinshijie/bili2text)，将B站中科目二、科目三的驾考培训视频转为文本数据。

![rag_raw_data.png](../assets/rag_raw_data.png)

### 处理原始数据

手工整理、整合数据，将所有数据统一为`txt`格式。

## 微调数据集

> **[通过Google Drive访问我们微调阶段的数据集](https://drive.google.com/drive/folders/1g0N1qDH0WYPYmCthUZdDtVSolfOKo-UH?usp=sharing)**

### 原始数据

网络上搜集的驾考科目一、科目四选择题题库。其中有一部分题库只有选项答案没有解析，另部分有答案解析。

为了在进行指令跟随微调后，TRLLM模型能针对用户的提问，不仅要给出正确的回答，还需要给出详细的解释。因此我们将有解析的科目一科目四题库制作为用作
**指令跟随微调的数据集**，而只有答案没有解析的科目一科目四题库我们将其制作为**评测数据集**用来评测微调和量化后TRLLM的性能。

- 没有解析的科目一题库：共1853条选择题。
- 没有解析的科目四题库：共1590条选择题。
- 有解析的科目一题库：共1615条选择题。
- 有解析的科目四题库：共1383条选择题。

上述题库中，其中有部分看图答题的题目，在后续制作文本数据集时进行了过滤，因此有一定的数据损失。

### 处理原始数据

#### Doc转markdown格式

对于用作微调用途的，有解析的题库，首先我们使用[doc转md格式的在线工具](https://products.aspose.app/words/conversion/word-to-md)
，将doc转换为更为结构化的文本，以便于后续的处理。

#### markdown转raw_json

> 由代码[mdtorawjson.py](mdtorawjson.py)实现。

- **功能描述**：[mdtorawjson.py](mdtorawjson.py)的主要功能是从一系列 Markdown 文件中提取题目文本，并将其格式化为 JSON
  数据结构，用于后续的数据处理和分析。
    1. **读取Markdown文件**：首先读取经过转换的科目一科目四题库 Markdown 文件。文件路径存储在 `file_names` 列表中。
    2. **内容拼接**：将所有读取到的文件内容拼接成一个长字符串，文件之间用换行符 `\n` 分隔，以便后续处理。
    3. **题号匹配与校验**：使用正则表达式 `\n\d+、`
       匹配文本中所有可能的题号。这些题号用于后续将文本分割成单独的问题。同时，通过 `check_question_number`
       函数校验题号的连续性和完整性，确保没有遗漏或错误的题号。
    4. **问题分割**：基于匹配到的题号，将拼接后的文本分割成独立的问题。每个问题都是字符串中的一个片段。
    5. **格式化与JSON转换**：对分割出的每个问题进行格式化处理，包括去除多余的空格和将换行符替换为 `\\n`。然后，将每个问题封装成一个
       JSON 对象，其中包含问题编号 (`no`) 和格式化后的问题文本 (`text`)。
    6. **保存到JSON文件**：将所有问题的 JSON 对象集合转换成 JSON
       格式的字符串，并保存到`rawtext.json`文件中。这个过程中，`ensure_ascii=False` 参数确保非 ASCII 字符（如中文）能够正确保存。
- 范例数据格式：

```json
[
  {
    "no": "1",
    "text": "1、对未取得驾驶证驾驶机动车的，会追究其法律责任。\\n\\nA、正确 \\n\\nB、错误 \\n\\n【答案】A \\n\\n【技巧 1】无证禁止驾车，违反依法追责。\\n\\n【技巧 2】解析：未取得驾驶证驾驶机动车，属于“无证驾驶”，将依法追究 法律责任。\\n\\n【讲解 1】本题主要考察无证驾驶的处罚。未取得驾驶证驾驶机动车属于违法 行为，将依法追究法律责任。因此选择“正确”。 \\n\\n【讲解 2】相关法规参考：《道路交通安全法》第九十九条，未取得机动车驾驶证、机动车驾驶证被吊销或者机动车驾驶证被暂扣期间驾驶机动车的，由公 安机关交通管理部门处二百元以上二千元以下罚款，可以并处十五日以下拘留。"
  },
  {
    "no": "2",
    "text": "2、驾驶机动车应随身携带哪种证件？\\n\\nA、工作证 \\n\\nB、驾驶证 \\n\\nC、身份证 \\n\\nD、职业资格证\\n\\n【答案】B \\n\\n【技巧 1】两证两标一号牌，不带扣车还罚款。\\n\\n【技巧 2】解析：驾驶机动车应随车携带机动车行驶证、驾驶证，无论是电子 版，还是纸质版，都需要随车携带。\\n\\n【讲解 1】本题主要考察机动车上路行驶条件。驾驶机动车上路行驶应随车携 带驾驶证、行驶证。因此选择“驾驶证”。 \\n\\n【讲解 2】相关法规参考：《道路交通安全法》第十九条，驾驶人应当按照驾 驶证载明的准驾车型驾驶机动车；驾驶机动车时，应当随身携带机动车驾驶 证。"
  }
]
```

#### raw_json转struc_json

> [strucjson.py](strucjson.py)

#### struct_json转finetune_json

> [makellmdata.py](makellmdata.py)



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