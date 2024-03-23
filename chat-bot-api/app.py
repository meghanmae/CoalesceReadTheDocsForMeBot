import os
from unittest import TestLoader
# Flask Imports
from flask import Flask
from flask_cors import CORS
# LangChain imports
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
# Local Imports
from endpoints import *

# Make sure to set API key in environment variables
# https://python.langchain.com/docs/integrations/chat/azure_chat_openai
from dotenv import load_dotenv
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)

def create_conversational_chain():
    # Directory for persisted index
    persist_directory = "persist"
    
    # Initialize the document loader.
    loader = DirectoryLoader("data/")

    embeddings = AzureOpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL_NAME"), 
        api_key=os.getenv("OPENAI_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        openai_api_type=os.getenv("OPENAI_API_TYPE"),
    )

    # Check for persisted index or create a new one
    if os.path.exists(persist_directory):
        print("Reusing index...")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        print("Creating new index...")
        index_creator = VectorstoreIndexCreator(
            vectorstore_kwargs={
                "persist_directory": persist_directory,
            }
        )
        vectorstore = index_creator.from_loaders([loader])
    
    # Setup the Azure OpenAI chat model.
    llm = AzureChatOpenAI(
        deployment_name=os.getenv("DEPLOYMENT_NAME"),
        model_name=os.getenv("DEPLOYMENT_NAME"),
        openai_api_base=os.environ.get("AZURE_ENDPOINT")
    )
    
    # Create the Conversational Retrieval Chain.
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    
    return chain


chain = create_conversational_chain()

# Routes
@app.route('/chat', methods=['POST'])
def chat():
    return endpoints.chat(chain)

@app.route('/scrape', methods=['POST'])
def scrape():
    return endpoints.scrape()
  
if __name__ == '__main__':
    app.run()