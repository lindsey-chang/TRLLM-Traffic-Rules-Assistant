# 基于xtuner的微调笔记
## TRLLM-v1模型微调过程
```bash
xtuner train internlm2_chat_7b_qlora_TRLLM_e1.py --deepspeed deepspeed_zero2
xtuner convert pth_to_hf internlm2_chat_7b_qlora_TRLLM_e1.py ./work_dirs/internlm2_chat_7b_qlora_TRLLM_e1/iter_2989.pth ./hf
xtuner convert merge /root/share/model_repos/internlm2-chat-7b ./hf ./merged --max-shard-size 2GB
xtuner chat ./merged --temperature 0.8 --top-p 0.8 --repetition-penalty 1.002 --prompt-template internlm2_chat
```

- 基于internml2-chat-7b进行QLoRA微调，
- 使用llm_conversation_dataset_merge_random_v1.json数据集（包括科目一科目四带解释版题库和自我认知数据集，打乱顺序后混合而成）上进行微调，为了增加数据量将相同数据复制了10遍，共「40468」条数据，训练一个批次。
- 生成了第一版的模型TRLLM-v1

## TRLLM-v2模型微调过程

```bash
xtuner train internlm2_chat_7b_qlora_TRLLM_e3.py --deepspeed deepspeed_zero2
xtuner convert pth_to_hf internlm2_chat_7b_qlora_TRLLM_e3.py ./work_dirs/internlm2_chat_7b_qlora_TRLLM_e3/iter_2989.pth ./hf
xtuner convert merge /root/share/model_repos/internlm2-chat-7b ./hf ./merged --max-shard-size 2GB
xtuner chat ./merged --temperature 0.8 --top-p 0.8 --repetition-penalty 1.002 --prompt-template internlm2_chat
```
- 基于internml2-chat-7b进行QLoRA微调
- 使用llm_conversation_dataset_merge_random_new.json数据集（包括科目一科目四带解释版题库、基于商业大模型改进output表述的数据集、和自我认知数据集，打乱顺序后混合而成）上进行微调，共「33834」条数据，训练三个批次。
- 生成了第二版的模型TRLLM-v2



