# Xlab部署
正如在[rag](../rag)目录下所说，Multi Query Retriever的表现取决于生成的额外提问，并且有时候不稳定，为了良好的用户体验，在xlab上部署的是 Ensemble Retriever版本

此文件夹中收录部署到xlab上所需要的文件夹 （作为备用）

`traffic_assistant_xlab-TRLLM-v2-EnsembleRetriever` ：基于internlm2-chat-7b 微调的 TRLLM-v2 

`traffic_assistant_xlab-TRLLM-v2-W4A16-EnsembleRetriever` ： TRLLM-v2 的 4bit 量化版本

## Xlab 仓库
如果需要部署到xlab，请 `git clone` 以下对应的链接
[traffic_assistant_xlab-TRLLM-v2-EnsembleRetriever](https://github.com/tackhwa/traffic_assistant_xlab/tree/TRLLM-v2-EnsembleRetriever)

[traffic_assistant_xlab-TRLLM-v2-W4A16-EnsembleRetriever](https://github.com/tackhwa/traffic_assistant_xlab/tree/TRLLM-v2-W4A16-EnsembleRetriever)

## Xlab 体验地址
[traffic_assistant_xlab-TRLLM-v2-EnsembleRetriever](https://openxlab.org.cn/apps/detail/tackhwa00/TRLLM-v2-Traffic-Assistant)

[traffic_assistant_xlab-TRLLM-v2-W4A16-EnsembleRetriever](https://openxlab.org.cn/apps/detail/tackhwa00/TRLLM-v2-W4A16-Traffic-Assistant)
