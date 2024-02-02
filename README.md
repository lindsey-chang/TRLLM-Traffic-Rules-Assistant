# TRLLM-Traffic-Rules-Assistant
<!-- PROJECT SHIELDS -->



<!-- PROJECT LOGO -->

<div align="center">
  <a href="https://github.com/lindsey-chang/TRLLM-Traffic-Rules-Assistant">
    <img src="assets/logo.png" alt="Logo" width="30%">
  </a>
<h3 align="center">TRLLM</h3>
</div>
<p>
<b>TRLLM</b> 是一款可以作为车载应用平台上的交规小助手，它专注于回答用户关于交通法规、道路驾驶技能以及机动车驾驶证考核内容的虚拟助手</br>
<b>TRLLM</b> 对于有意考取驾驶证的同学，TrafficBot-InternLM是不可或缺的选择。其以题目问答解答为特色，为想深入了解交通法规的同学提供了专业支持
</p>

项目LOGO由DALL·E生成:
- Prompt:
> I want a logo for a github project called Traffic-Rules-Assistant. 
>
> I want it to look minimal and tech-based. It should be clear enough to be legible in a small profile avatar. Please make the logo fit within a circle. The border of the circular logo represents the steering wheel, and the interior of the circular logo draws a robot to represent the large language model (There should be more emphasis on the features of the steering wheel, and the robot can just be represented figuratively with sketch lines). Use the colors black and variations of blue for the circular logo, and the background color should be clean white.
>
> The main logo should just contain the letters: "TRLLM".  "TRLLM" needs to be directly below the circular logo!!! Both the circular LOGO and the "TRLLM" text should be centered in the vertical direction (y-axis direction).
 

## Reference
[https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both](https://www.rungalileo.io/blog/optimizing-llm-performance-rag-vs-finetune-vs-both)



##  Features
- [**监督微调**]()：我们的数据集包含了科目一和科目四的题库。为了进一步提高数据集的质量，我们利用现有商业大模型api对数据集进行了扩展。这一扩展使得数据更加贴近人类提问的语言习惯，并确保问题的逻辑前后语序更为连贯。在这个基础上，我们进行了对InternLM2-chat-7B的监督微调。
- [**检索增强生成**](): 我们建立了一个向量数据库，其中包含有关《中华人民共和国公安部令》和《中华人民共和国国务院令》的相关交通法规，以及机动车驾驶证考核相关的资料，流程，以及诀窍。基于langchain技术，我们构建了一个多查询混合搜索的检索架构，以提高信息检索的准确性以多样性。
- [**量化模型**]()：我们使用LMDeploy工具对微调后的模型进行W4A16量化，以在实际部署中提高模型的效率和性能。
- [**客观评测**]()：我们使用opencompass对模型进行了客观评估，考察其在各种测试条件下的准确性，同时比较了模型在量化前后的性能表现。


##  Release Models
| Model(ModelScope)                                                                                           | Introduction                                                                                                   | 
|:------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------|
| [TRLLM-v1-InternLM-chat-7B-Merged]()                                                                          |    在[llm_conversation_dataset_merge_random_v1.json]()上微调了一版InternLM2-chat-7B模型，发布完整权重                                 |
| [TRLLM-v1InternLM-chat-7B-Merged-4bit]()                                                                      |  在TRLLM-v1-InternLM-chat-7B-Merged的基础上进行W4A16量化，发布完整权重                             |

## 目录
- [TRLLM-交规小助手]()
  - [**环境配置**]()
  - [**使用指南**]()
    - [文件目录说明]()
    - [数据构建]()
    - [微调指南]()
    - [量化指南]()
    - [部署指南]()

