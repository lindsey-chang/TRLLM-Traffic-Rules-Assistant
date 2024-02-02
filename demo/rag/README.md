### 进到目录下
`cd TRLLM-Traffic-Rules-Assistant/demo/rag`

### 创建环境
`conda env create --name traffic_assistant_rag --file=environment.yml` <br>
`conda activate traffic_assistant_rag` <br>
`pip install -r requirements.txt`

### 下载所需模型（internlm2-chat-7b，sentence-transformer）
`python model_download.py`

### 创建vector_db数据集以及bm25检索会用到的combine.txt
`python create_db.py`

### streamlit，启动！
`streamlit run web_demo.py --server.address 127.0.0.1 --server.port 6006`
