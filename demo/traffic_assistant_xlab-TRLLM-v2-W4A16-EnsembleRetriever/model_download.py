import os

# 设置环境变量
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载sentence-transformer模型
os.system('huggingface-cli download --resume-download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --local-dir /home/xlab-app-center/model/sentence-transformer')

# 下载InternLM-chat-7b模型
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
model_dir = snapshot_download('heitao5200/TRLLM-Model-4bit_turbomind', cache_dir='/home/xlab-app-center/model')
