"""
This script refers to the dialogue example of streamlit, the interactive generation code of chatglm2 and transformers.
We mainly modified part of the code logic to adapt to the generation of our model.
Please refer to these links below for more information:
    1. streamlit chat example: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
    2. chatglm2: https://github.com/THUDM/ChatGLM2-6B
    3. transformers: https://github.com/huggingface/transformers
"""
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from dataclasses import asdict

import streamlit as st
import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging
import logging as lg
from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from tools.transformers.interface import GenerationConfig, generate_interactive

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from OutputParser import LineListOutputParser
from langchain.chains import LLMChain
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from lmdeploy import turbomind as tm

logger = logging.get_logger(__name__)



class InternLM_LLM(LLM):
    tm_model:None= None
    generator:None = None
    def __init__(self,tm_model,generator):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        super().__init__()
        self.tm_model=tm_model
        self.generator=generator

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数

        prompt_t = self.tm_model.model.get_prompt(prompt)        
        input_ids = self.tm_model.tokenizer.encode(prompt_t)
        for outputs in self.generator.stream_infer(session_id=0,input_ids=[input_ids]):            
            response = self.tm_model.tokenizer.decode(outputs[1])            
        return response
        # for outputs in self.generator.stream_infer(session_id=0,input_ids=[input_ids]):
        #     res, tokens = outputs[0]
        # response = self.tm_model.tokenizer.decode(res.tolist())
        # return response

    @property
    def _llm_type(self) -> str:
        return "InternLM"

def load_chain(tm_model,generator):
    # 加载问答链
    # 定义 Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    with open("./dataset/rag_data_base/combine.txt") as f:
        docs = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=300)

    texts = text_splitter.create_documents([docs])

    bm25_retriever = BM25Retriever.from_documents(texts)
    bm25_retriever.k =  2

    # 向量数据库持久化路径
    persist_directory = './dataset/rag_data_base/vector_db/rag_datasets'

    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
        embedding_function=embeddings
    )

    retriever_chroma=vectordb.as_retriever(search_kwargs={"k": 2})

    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_chroma],
                                       weights=[0.4, 0.6])
    
    # 加载自定义 LLM
    llm = InternLM_LLM(tm_model,generator)

    # 定义一个 Prompt Template
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。请提供详细而清晰的回答。确保回答涵盖相关法规和实际技能，尽量详细回答问题，并尽量避免简单带过问题。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    有用的回答:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    # 运行 chain
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=ensemble_retriever, return_source_documents=True,
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

    return qa_chain


def on_btn_click():
    del st.session_state.messages


@st.cache_resource
def load_model():
    tm_model = tm.TurboMind.from_pretrained(pretrained_model_name_or_path="./model/heitao5200/TRLLM-Model-4bit_turbomind/workspace_trll2_model_4bit_turbomind",trust_remote_code=True)
    generator = tm_model.create_instance()
    return tm_model, generator


def prepare_generation_config():
    with st.sidebar:
        # max_length = st.slider("Max Length", min_value=32, max_value=2048, value=2048)
        # top_p = st.slider("Top P", 0.0, 1.0, 0.8, step=0.01)
        # temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.01)
        st.button("Clear Chat History", on_click=on_btn_click)
        enable_rag=st.checkbox('RAG检索')
        

    # generation_config = GenerationConfig(max_length=max_length, top_p=top_p, temperature=temperature,repetition_penalty=1.002)

    return enable_rag


user_prompt = '<|im_start|>user\n{user}<|im_end|>\n'
robot_prompt = '<|im_start|>assistant\n{robot}<|im_end|>\n'
cur_query_prompt = '<|im_start|>user\n{user}<|im_end|>\n\
    <|im_start|>assistant\n'


def combine_history(prompt):
    messages = st.session_state.messages
    meta_instruction = ('You are InternLM (书生·浦语), a helpful, honest, '
                        'and harmless AI assistant developed by Shanghai '
                        'AI Laboratory (上海人工智能实验室).')
    total_prompt = f"<s><|im_start|>system\n{meta_instruction}<|im_end|>\n"
    for message in messages:
        cur_content = message['content']
        if message['role'] == 'user':
            cur_prompt = user_prompt.format(user=cur_content)
        elif message['role'] == 'robot':
            cur_prompt = robot_prompt.format(robot=cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.format(user=prompt)
    return total_prompt

def main():
    # torch.cuda.empty_cache()
    print("load model begin.")
    tm_model, generator = load_model()
    qa_chain=load_chain(tm_model, generator)
    print("load model end.")

    user_avator = "./imgs/user.png"
    robot_avator = "./imgs/robot.png"

    st.title("TRLLM-v2-4bit-交通规则助手大语言模型")

    enable_rag = prepare_generation_config()

    # enable_rag=st.checkbox('RAG检索')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user", avatar=user_avator):
            st.markdown(prompt)
        real_prompt = combine_history(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_avator})

        if enable_rag:
            with st.chat_message("robot", avatar=robot_avator):
                message_placeholder = st.empty()
                cur_response=qa_chain({"query": prompt})["result"]
                message_placeholder.markdown(cur_response)
        else:
            with st.chat_message("robot", avatar=robot_avator):
                message_placeholder = st.empty()
                tm_prompt = tm_model.model.get_prompt(prompt)
                input_ids = tm_model.tokenizer.encode(tm_prompt)
                for outputs in generator.stream_infer(session_id=0,input_ids=[input_ids]): 
                    cur_response = tm_model.tokenizer.decode(outputs[1])
                    # Display robot response in chat message container
                    message_placeholder.markdown(cur_response + "▌")
                message_placeholder.markdown(cur_response)

        # Add robot response to chat history
        st.session_state.messages.append({"role": "robot", "content": cur_response, "avatar": robot_avator})
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
