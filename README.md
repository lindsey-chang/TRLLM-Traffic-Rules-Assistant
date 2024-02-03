<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/lindsey-chang/TRLLM-Traffic-Rules-Assistant">
    <img src="assets/logo.png" alt="Logo" width="30%">
  </a>
<h3 align="center">TRLLM</h3>
</div>

<!-- PROJECT SHIELDS -->
<!-- PROJECT SHIELDS -->
![](https://img.shields.io/badge/language-python-orange.svg)<span>&nbsp;&nbsp;</span>
![](https://img.shields.io/github/languages/top/lindsey-chang/TRLLM-Traffic-Rules-Assistant.svg?style=flat-square)<span>&nbsp;&nbsp;</span>
![](https://img.shields.io/github/contributors/lindsey-chang/TRLLM-Traffic-Rules-Assistant.svg?style=flat-square)<span>&nbsp;&nbsp;</span>
![](https://img.shields.io/github/forks/lindsey-chang/TRLLM-Traffic-Rules-Assistant.svg?style=flat-square)<span>&nbsp;&nbsp;</span>
![](https://img.shields.io/github/issues/lindsey-chang/TRLLM-Traffic-Rules-Assistant.svg?style=flat-square)<span>&nbsp;&nbsp;</span>
![License](https://img.shields.io/badge/license-MIT-green.svg)<span>&nbsp;&nbsp;</span>
![](https://img.shields.io/github/stars/lindsey-chang/TRLLM-Traffic-Rules-Assistant.svg?style=flat-square)

<p>
<b>TRLLM</b> 是一款可以作为车载应用平台上的交规小助手，它专注于回答用户关于交通法规、道路驾驶技能以及机动车驾驶证考核内容。</br>
对于有意向考取驾驶证的同学，<b>TRLLM</b>是不可或缺的选择。其以为科目一考题、科目四考题、公安部与国务院发布交通法规和科目二科目三教学视频文本为数据集来源，为想深入了解交通法规的同学提供了专业支持。
</p>

---

## Features

- [**经过筛选的高质量结构化交通知识数据集**](./dataset/)
  ：我们的数据集包含了科目一和科目四的题库，对原始题库，我们进行了一系列的JSON结构化（`TRLLM-v1`
  的训练数据集）。为了进一步提高数据集的质量，我们利用现有商业大模型api对数据集进行了扩展。这一扩展使得数据更加贴近人类提问的语言习惯，并确保问题的逻辑前后语序更为连贯（`TRLLM-v2`
  的训练数据集）。另外，我们还生成了自我认知数据集。根据另一份只有答案没有解析的科目一科目四选择题题库，自制了客观评测数据集，用于评测比较TRLLM与InternLM2-chat-7B在交通知识上的客观推理能力。用于微调和评测的数据集分开制作没有交叉，确保评测结果真实可靠。
- [**有监督微调**](./finetune/)：基于上述三种数据集，我们以InternLM2-chat-7B为基座模型进行了有监督微调。TRLLM-Model-v1是基于科目一科目四题库解析、自我认知数据集的。TRLLM-Model-v2是基于商业大模型api扩展数据集和自我认知数据集的。
- [**检索增强生成**](./rag/):
  我们建立了一个向量数据库，其中包含有关《中华人民共和国公安部令》和《中华人民共和国国务院令》的相关交通法规，以及机动车驾驶证考核相关的资料，流程，以及诀窍。基于langchain技术，我们构建了一个多查询混合搜索的检索架构，以提高信息检索的准确性以多样性。
- [**量化模型**](./quant/)：我们使用LMDeploy工具对微调后的模型进行W4A16量化和KV Cache量化，以在实际部署中降低模型的显存开销和提高模型的运行效率。
- [**客观评测**](./evaluation/)：我们使用OpenCompass对模型进行了客观评测，考察其在科目一和科目四考试题库下做选择题`MCQ`
  的准确性，同时对比较了TRLLM-Model的4个不同的版本`TRLLM-v1`、`TRLLM-v2`、`TRLLM-v1-4bit`量化版本、`TRLLM-v2-4bit`
  量化版本和`InternLM-chat-7b`在我们自制的评测数据集上的准确率表现，从而评估TRLLM基于交通知识进行微调的效果，并判断这4种TRLLM-Model哪一个准确率最高，可以部署在生产应用场景。**经过客观评测，我们得出了`TRLLM-v2`的准确率最高**。

## Released Models

| Model(ModelScope) | Introduction                                                                       |
|:------------------|:-----------------------------------------------------------------------------------|
| [TRLLM-v1]()      | 在[llm_conversation_dataset_merge_random_v1.json]()上微调了一版InternLM2-chat-7B模型，发布完整权重 |
| [TRLLM-v1-4bit]() | 在TRLLM-v1-InternLM-chat-7B-Merged的基础上进行W4A16量化，发布完整权重                              |
| [TRLLM-v2]()      | 在[llm_conversation_dataset_merge_random_v1.json]()上微调了一版InternLM2-chat-7B模型，发布完整权重 |
| [TRLLM-v2-4bit]() | 在TRLLM-v1-InternLM-chat-7B-Merged的基础上进行W4A16量化，发布完整权重                              |

---

## 如何体验本项目

### 1. 克隆本项目到您的本地开发机上

```bash
git clone https://github.com/lindsey-chang/TRLLM-Traffic-Rules-Assistant.git
```

默认所有 web_demo 脚本运行的都是 TRLLM-v2 模型，可根据提供的模型下载链接自行下载替换不同版本的模型。

#### 配置环境

```bash
conda env create --name traffic_assistant_rag --file=environment.yml
conda activate traffic_assistant_rag
pip install -r requirements.txt
python download_turbomind.py
```

#### 启动 Streamlit

```bash
streamlit run web_demo_ensemble_retriever.py --server.address 127.0.0.1 --server.port 6006
```

### 2. 在OpenXlab上体验本项目

[TRLLM-v2-Traffic-Assistant](https://openxlab.org.cn/apps/detail/tackhwa00/TRLLM-v2-Traffic-Assistant)

#### 运行结果摘要
可以在左侧设置是否开启RAG

![xlab.png](assets/xlab.png)
![xlab-1.png](assets/xlab-1.png)
![xlab-2.png](assets/xlab-2.png)

### 3. Xtuner chat体验微调后的模型

使用Xtuner chat直接测试发布在Model Scope上的TRLLM模型。

#### 运行结果摘要

![chat_3.png](assets/chat_3.png)
![chat_2.png](assets/chat_2.png)
![chat_1.png](assets/chat_1.png)

---

## TRLLM-Traffic-Rules-Assistant 构建逻辑

### 项目结构

### 数据构建

### 微调指南

### 量化部署

#### 4bit 量化

- 计算 minmax
- 量化权重模型
- 量化后的模型转换成turbomind 格式
- 启动4bit量化后的模型

#### KV Cache 量化

- 转换原始模型格式
- 计算 minmax
- 获取量化参数（注意此时是把结果放到 turbomind的模型weight目录下
- 修改参数
- 启动kvcache量化之后的模型

#### 4bit 量化 + KV Cache 量化

- 获取量化参数（注意此时是把结果放到 4bit 量化turbomind的模型weight目录下
- 启动4bit+kvcache模型

### 评测分析

### 问题思考

## Reference

[https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both](https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both)

---

## 后记

项目LOGO由DALL·E生成:

- Prompt:

> I want a logo for a github project called Traffic-Rules-Assistant.
>
> I want it to look minimal and tech-based. It should be clear enough to be legible in a small profile avatar. Please
> make the logo fit within a circle. The border of the circular logo represents the steering wheel, and the interior of
> the circular logo draws a robot to represent the large language model (There should be more emphasis on the features
> of
> the steering wheel, and the robot can just be represented figuratively with sketch lines). Use the colors black and
> variations of blue for the circular logo, and the background color should be clean white.
>
> The main logo should just contain the letters: "TRLLM".  "TRLLM" needs to be directly below the circular logo!!! Both
> the circular LOGO and the "TRLLM" text should be centered in the vertical direction (y-axis direction).
