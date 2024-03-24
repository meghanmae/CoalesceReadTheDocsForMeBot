import os
from unittest import TestLoader
# Flask Imports
from flask import Flask
from flask_cors import CORS

# Local Imports
from endpoints import *

from dotenv import load_dotenv
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)

# Routes
@app.route('/chat', methods=['POST'])
def chat():
    return endpoints.chat()

@app.route('/scrape', methods=['POST'])
def scrape():
    return endpoints.scrape()
  
if __name__ == '__main__':
    app.run()