import os
os.system("python model_download.py")
os.system('streamlit run app.py --server.address=0.0.0.0 --server.port 7860')

