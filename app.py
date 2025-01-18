from flask import Flask, render_template, request, jsonify 
import os
from langchain_openai import OpenAIEmbeddings 
from langchain_community.vectorstores import Chroma 
from langchain.chains.question_answering import load_qa_chain 
from langchain_community.callbacks import get_openai_callback 
from langchain_openai import ChatOpenAI 
from opencc import OpenCC
import openai
from openai import OpenAI
client = OpenAI ( )
openai.api_key = os. getenv('OPENAI_API_KEY')

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({'error': 'No user input provided'})
    
    try:
        # 設置嵌入模型與檢索數據庫
        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)
        
        # 進行相似度檢索
        docs = db.similarity_search(user_input)
        
        # 使用 ChatOpenAI 啟動生成模型
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
        chain = load_qa_chain(llm, chain_type="stuff")
        
        with get_openai_callback() as cb:
            response = chain.invoke({"input_documents": docs, "question": user_input}, return_only_outputs=True)
        
        # 簡繁體轉換
        cc = OpenCC('s2t')
        answer = cc.convert(response['output_text'])
        
        return jsonify({'response': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)})
