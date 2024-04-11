from dotenv import load_dotenv

load_dotenv()

import asyncio
import os
import erniebot
from openai import OpenAI

class OpenAIChat:
    def __init__(self,glm=None):
        if glm is None:
            raise RuntimeError("OpenAIApi is Error!")
        self.glm = glm


    async def _aask(self, prompt, stream=False, model="gpt-3.5-turbo", top_p=0.95):
        messages = [{"role": "user", "content": prompt}]
        response = self.glm.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            top_p=top_p
        )
        return response.choices[0].message.content


class BaiduApi:
    def __init__(self):
        pass

    async def _aask(self, prompt, stream=False, model="ernie-3.5", top_p=0.95):
        messages = [{"role": "user", "content": prompt}]
        response = erniebot.ChatCompletion.create(
            model=model, messages=messages, top_p=top_p, stream=stream
        )
        return response.result



class LLMApi:
    def __init__(self):
        self.llm_api = None

        # if os.environ["OPENAI_API_KEY"] is not None:
        #     glm = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        #     self.llm_api = OpenAIChat(glm)

        # select api
        if os.environ["BAIDU_API_KEY"] is not None:
            erniebot.api_type = "aistudio"
            erniebot.access_token = os.environ["BAIDU_API_KEY"]
            self.llm_api = BaiduApi()
        else:
            raise RuntimeError("No api_key found!")

    async def _aask(self, prompt, stream=False, top_p=0.95):
        rsp = await self.llm_api._aask(prompt, stream=stream, top_p=top_p)
        return rsp


if __name__ == "__main__":
    # models = erniebot.Model.list()
    # print("可用模型",models)

    llm_api = LLMApi()
    # result = asyncio.run(baidu_api._aask("你好啊"))
    result = asyncio.run(llm_api._aask("你好啊"))
    print("result", result)
