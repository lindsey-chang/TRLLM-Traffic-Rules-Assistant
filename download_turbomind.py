

# 下载InternLM-chat-7b模型
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
model_dir = snapshot_download('heitao5200/TRLLM-Model-4bit_turbomind', cache_dir='./model')
