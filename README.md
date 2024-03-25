# CoalesceReadTheDocsForMeBot
A bot powered by Open AI's ChatGPT to answer questions about the coalesce documentation

## Setup
**Install Python**
- https://www.python.org/downloads/
- Be sure to click 'Add Python 3.x to PATH' when doing the install

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
The API endpoint is hardcoded under [scripts/useAxios.ts](https://github.com/meghanmae/CoalesceReadTheDocsForMeBot/blob/d4825d7e465954df217221ec6e46ead3213f2119/chat-bot-ui/src/scripts/useAxios.ts#L4)... so make sure the magic string matches your API port

**Troubleshooting**
If you get an error similar to `ValueError: Collection coalesce_docs does not exist.` you may have to call the scrape method to trigger chroma DB to generate your vectors. You can do this in the _playground.py file or with the scrape endpoint. 
