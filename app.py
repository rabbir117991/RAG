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
@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(message = 'Hello World !')

if __name__ == '__main__':
  app.run(debug=True)

def get_response):
user_input = request.form.get(user_input')
db = None
if not user_input:
return jsonify({'error': 'No user input provided'})
if user_input:
embeddings = OpenAlEmbeddings)
db = Chroma(persist_directory="./db/temp/",
", embedding_function=embeddings)
docs = b.similarity_search(user_input)
Ilm = ChatOpenAl(
model_name="gpt-4o"
temperature=0.5
chain = load_qa_chain(lIm, chain_type="stuff")
with get_openai_callback() as cb:
response = chain.invoke({"input_documents": docs, "question":user_input}, return_only_outputs=True)
cc = OpenCC('s2t')
answer=cc.convert(response|output_text'])
chat_history.append(f'user': user_input, 'assistant': response['output_text']})
return jsonify({'response': answer})
