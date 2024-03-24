# CoalesceReadTheDocsForMeBot
A bot powered by Open AI's ChatGPT to answer questions about the coalesce documentation

## Setup
**API**
1. Navigate to the chat-bot-api directory and run `pip install -r requirements.txt` to install dependencies 

2. Configure the following environment variables in a `.env` file
```
AZURE_OPENAI_API_KEY
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_REGION
AZURE_OPENAI_DEPLOYMENT_NAME
AZURE_OPENAI_API_VERSION
```

**Client**
1. Navigate to the chat-bot-ui directory and run `npm i` to install dependencies

## Running the app
**Run the API**
Navigate to the chat-bot-api directory and run `python app.py`

**Run the Client**
Navigate to the chat-bot-ui directory and run `npm run dev`
