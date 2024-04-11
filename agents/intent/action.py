from typing import Optional, Any
import json
import sys
from metagpt.actions import Action
from metagpt.logs import logger
from dotenv import load_dotenv
sys.path.append('./TRLLM-Traffic-Rules-Assistant')
from utils.common_llm_api import LLMApi

load_dotenv()

# 设计思路 给定人设并导入参考聊天话术、历史聊天语料进行聊天。
class RecvAndAnalyze(Action):
    PROMPT_TEMPLATE: str = """
    任务描述：你是一个意图分析助手，你需要根据用户输入的文本，分析其意图并返回以下结果：

    “1”：如果用户提问关于普遍交通知识
    “2”：如果用户提问关于交通法规
    “3“：如果用户提问路面情况（路牌识别）

    分析要求：你需要根据历史消息记录中的用户提问，判断其属于哪种类型。

    示例：
        普遍交通知识:
            1. 当车辆前轮爆胎导致车辆开始转向时，作为驾驶员，你应该怎么做才能尽量保持车辆直线行驶？
            2. 在无交通信号指示的交叉路口，若机动车需要转弯，应如何处理直行车辆和行人？
            3. 机动车在准备向左转弯、变更车道、驶离停车地点或掉头的时候，为什么要提前开启左转向灯？
        
        交通法规:
            1. 驾驶机动车不按规定使用灯光，会被扣掉几分？
            2. 如果驾驶机动车违反了禁令标志或禁止标线指示，会被扣多少分？
            3. 酒驾会被罚多少？
            
        路面情况（路牌识别）:
            1. 这是什么路牌？
            2. 这段路可以鸣笛吗？
            3. 这里可以180度轉彎吗？

    历史消息记录如下```
    {instruction}
    ```
    请认真结合历史消息分析最新的用户意图。以上示例仅供参考，你需要自己思考用户的意图。
    只需要回复我数字”1“，”2“，”3“的其中一个，不需要回复其他任何带文字的内容！
    如果用户的意图都不是以上三个，请只返回数字”1“，不需要回复其他任何带文字的内容！
    """

    name: str = "RecvAndAnalyze"

    async def run(self, instruction: str):
        logger.info("instruction\n" + instruction)
        prompt = self.PROMPT_TEMPLATE.format(
            instruction=instruction
        )

        rsp = await LLMApi()._aask(prompt=prompt, top_p=0.1)
        # prefix = "intent recognition: "  
        # if rsp.startswith(prefix):  
        #     number = text[len(prefix):] 
        logger.info("机器人分析需求：\n" + rsp)
        return rsp

