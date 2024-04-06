import os

from openai import AzureOpenAI
from dotenv import load_dotenv

class OpenAIChatClient:
    def __init__(self):
        load_dotenv(override=True)
        self._client = self._get_client()
        self.system_prompt = """
        You are a chatbot that answers questions about Coalesce.
        You answer all code-related questions using Typescript and Vue Composition API unless asked otherwise. 
        You are concise and helpful, and always return citations for the id of the document you found information from.
        For example, for "id":"/Coalesce/introduction.html", return {"citation":"/Coalesce/introduction.html"} in your response.
        You always format your response using markdown. 
        If you don't know an answer, say I don't know.
    """

    def _get_client(self):
        client = AzureOpenAI(
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_key=os.environ.get("AZURE_OPENAI_KEY"),
        )
        return client
    
    def _get_completion(self, user_query, chat_history, documents):
        user_message = f"""
        Relevant documents:
        ---
        {documents}

        User query:
        {user_query}
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(chat_history)
        messages.append({"role": "user","content": user_message})

        chat_completion = self._client.chat.completions.create(
            messages=messages,
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
        )
        return chat_completion
    
    def _parse_completion(self, chat_completion):
        chat_completion
        return chat_completion.choices[0].message.content