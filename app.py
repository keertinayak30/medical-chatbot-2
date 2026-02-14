from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from src.prompt import *
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain

app = Flask(__name__)


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY=os.environ.get('GROQ_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


index_name = "medchatbot2" 

embeddings = None
docsearch = None
retriever = None
rag_chain = None

def init_rag():
    global embeddings, docsearch, retriever, rag_chain
    if embeddings is None:
        print("🔄 Initializing embeddings...")
        embeddings = download_hugging_face_embeddings()
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile", 
            groq_api_key=GROQ_API_KEY,
            temperature=0.3,
            streaming=True
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain



# embeddings = download_hugging_face_embeddings()

# docsearch = PineconeVectorStore.from_existing_index(
#     index_name=index_name,
#     embedding=embeddings
# )

# retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# llm = ChatGroq(
#     model_name="llama-3.3-70b-versatile", 
#     groq_api_key=GROQ_API_KEY,
#     temperature=0.3,
#     streaming=True
# )

memory = ConversationBufferWindowMemory(
    k=5, 
    memory_key="chat_history",
    return_messages=True
)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )

# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# conversation_chain = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     retriever=retriever,
#     combine_docs_chain_kwargs={
#         "prompt": ChatPromptTemplate.from_messages([
#             ("system", system_prompt),MessagesPlaceholder(variable_name="chat_history"),
#             ("human", "{context}\n\nQuestion: {question}")
#         ])
#     },
#     return_source_documents=True,
#     verbose=False 
# )


@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["POST"])  
def chat():
    global embeddings, docsearch, retriever, rag_chain
    
    if request.is_json:
        data = request.get_json()
        msg = data.get('msg', '')
    else:
        msg = request.form.get('msg', '')
    
    if not msg:
        return jsonify({"response": "Please enter a message!"}), 400
    
    print(f"User: {msg}")

    rag_chain = init_rag()

    recent_history = [h.content for h in memory.chat_memory.messages[-3:] if hasattr(h, 'content')]
    full_query = msg if len(recent_history) == 0 else f"{msg} (previous: {' '.join(recent_history[-1:])})"
    result = rag_chain.invoke({"input": full_query, "chat_history": memory.chat_memory.messages})

    response_text = result["answer"]
    print(f"Bot: {response_text}")
    
    memory.save_context(
        {"input": msg}, 
        {"output": response_text}
    )
    
    return jsonify({"response": response_text})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port= port, debug= True)