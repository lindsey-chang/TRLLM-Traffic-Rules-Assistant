__import__('pysqlite3')
import sys
import os
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from dataclasses import asdict
import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging
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


# os.system("python create_db.py")


class InternLM_LLM(LLM):
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None
    def __init__(self,model,tokenizer):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        super().__init__()
        self.tokenizer=tokenizer
        self.model=model
        self.model = self.model.eval()

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数
        system_prompt = """你是交通法则小助手，熟知中华人民共和国公安部令和国务院令的交通法规知识，以及详尽的道路驾驶技能和安全文明常识考试内容。
        """

        messages = [(system_prompt, '')]
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        return response

    @property
    def _llm_type(self) -> str:
        return "InternLM"

def load_chain(model,tokenizer):
    # 加载问答链
    # 定义 Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="/home/xlab-app-center/model/sentence-transformer")

    with open("/home/xlab-app-center/data_base/vector_db/rag_datasets/combine.txt") as f:
        docs = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=300)

    texts = text_splitter.create_documents([docs])

    bm25_retriever = BM25Retriever.from_documents(texts)
    bm25_retriever.k =  2

    # 向量数据库持久化路径
    persist_directory = '/home/xlab-app-center/data_base/vector_db/rag_datasets'

    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
        embedding_function=embeddings
    )

    retriever_chroma=vectordb.as_retriever(search_kwargs={"k": 2})

    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_chroma],
                                       weights=[0.4, 0.6])
    
    output_parser = LineListOutputParser()

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""你是一名人工智能语言模型助理。您的任务是基于给定用户提问生成额外三个尽可能短的不同版本的提问，
        以便从矢量数据库中检索相关文档。通过对用户问题生成多种观点，
        你的目标是帮助用户克服基于距离的相似性搜索的一些局限性。
        以以下形式输出提问，
        1：额外提问1，
        2：额外提问2，
        3：额外提问3，
        原本的用户提问： {question}""",
    )

    # 加载自定义 LLM
    llm = InternLM_LLM(model,tokenizer)

    llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT, output_parser=output_parser)

    multi_retriever = MultiQueryRetriever(retriever=ensemble_retriever, llm_chain=llm_chain,include_original=True)

    # 定义一个 Prompt Template
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。请提供详细而清晰的回答。确保回答涵盖相关法规和实际技能，尽量详细回答问题，并尽量避免简单带过问题。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    有用的回答:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    # 运行 chain
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=multi_retriever, return_source_documents=True,
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

    return qa_chain


def on_btn_click():
    del st.session_state.messages


@st.cache_resource
def load_model():
    model = (
        AutoModelForCausalLM.from_pretrained("/home/xlab-app-center/model/Shanghai_AI_Laboratory/internlm2-chat-7b", trust_remote_code=True)
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained("/home/xlab-app-center/model/Shanghai_AI_Laboratory/internlm2-chat-7b", trust_remote_code=True)
    return model, tokenizer


def prepare_generation_config():
    with st.sidebar:
        max_length = st.slider("Max Length", min_value=32, max_value=2048, value=2048)
        top_p = st.slider("Top P", 0.0, 1.0, 0.8, step=0.01)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.01)
        st.button("Clear Chat History", on_click=on_btn_click)
        enable_rag=st.checkbox('RAG检索')
        

    generation_config = GenerationConfig(max_length=max_length, top_p=top_p, temperature=temperature,repetition_penalty=1.002)

    return generation_config,enable_rag


user_prompt = "<|User|>:{user}\n"
robot_prompt = "<|Bot|>:{robot}<eoa>\n"
cur_query_prompt = "<|User|>:{user}<eoh>\n<|Bot|>:"


def combine_history(prompt):
    messages = st.session_state.messages
    total_prompt = ""
    for message in messages:
        cur_content = message["content"]
        if message["role"] == "user":
            cur_prompt = user_prompt.replace("{user}", cur_content)
        elif message["role"] == "robot":
            cur_prompt = robot_prompt.replace("{robot}", cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.replace("{user}", prompt)
    return total_prompt


def main():
    # torch.cuda.empty_cache()
    print("load model begin.")
    model, tokenizer = load_model()
    qa_chain=load_chain(model, tokenizer)
    print("load model end.")

    user_avator = "/home/xlab-app-center/imgs/user.png"
    robot_avator = "/home/xlab-app-center/imgs/robot.png"

    st.title("traffic-assistant")

    generation_config,enable_rag = prepare_generation_config()

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
                for cur_response in generate_interactive(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=real_prompt,
                    additional_eos_token_id=92542,
                    **asdict(generation_config),
                ):
                    # Display robot response in chat message container
                    message_placeholder.markdown(cur_response + "▌")
                message_placeholder.markdown(cur_response)

        # Add robot response to chat history
        st.session_state.messages.append({"role": "robot", "content": cur_response, "avatar": robot_avator})
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
