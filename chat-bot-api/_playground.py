from endpoints import endpoints

endpoints.scrape()

query = "How can I use it?"
relevant_docs = endpoints._query_collection(query)
ids = [doc["id"] for doc in relevant_docs]
print(ids)


from OpenAIChatClient import OpenAIChatClient

chat_client = OpenAIChatClient()

chat_history = [
    {"role": "user", "content": "What is Vite"},
    {
        "role": "assistant",
        "content": """
 Vite is the development and build tooling for your frontend Vue code in Coalesce. It enables lightning-fast single-page application development. Coalesce integrates ASP.NET Core and Vite together, streamlining local development to require nothing more than a `dotnet run` or a single-click launch in your IDE. Vite is based on the Vite Documentation (source). [^1^]

[^1^]: {"citation":"/Coalesce/introduction.html"}
 """,
    },
]
response = chat_client._get_completion(
    user_query=query, chat_history=chat_history, documents=relevant_docs
)

parsed_response = chat_client._parse_completion(response)
print(parsed_response)

print(f"Citations: {ids}")
