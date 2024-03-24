from flask import request
import requests
import bs4
import chromadb

from OpenAIChatClient import OpenAIChatClient

class endpoints:
    collection_name = "coalesce_docs"

    # region Chat Endpoint
    @staticmethod
    def chat():
        chat_client = OpenAIChatClient()
        data = request.get_json()
        query = data["message"]
        chat_history = data["chat_history"]

        # Note: Chat history is expected to follow the format List[dict[str:str]], with keys "role" and "content". "role" can be 'user' or 'assistant'.
        #[ {"role": "user", "content": "What is Vite"}, {"role": "assistant", "content": "Vite is this"}]

        relevant_docs = endpoints._query_collection(query)

        response = chat_client._get_completion(
            user_query=query, chat_history=chat_history, documents=relevant_docs
        )

        parsed_response = chat_client._parse_completion(response)

        return parsed_response
    
    @staticmethod
    def _query_collection(query:str, n_results=3):
        chroma_client = chromadb.PersistentClient(path="persist")
        try:
            collection = chroma_client.get_collection(endpoints.collection_name)
        except ValueError as e:
            print("Collection does not exist!")
            raise e
        results = collection.query(query_texts=query, n_results=n_results)
        formatted_results = endpoints._format_collection_results(results)
        return formatted_results
    
    @staticmethod
    def _format_collection_results(results):
        documents = results["documents"][0]
        ids = results["ids"][0]

        formatted_query_results = [
            {"id": ids[i], "document": documents[i]} for i in range(len(documents))
        ]
        return formatted_query_results

    # endregion

    # region Scrape Endpoint
    @staticmethod
    def scrape():
        siteUrl = "https://intellitect.github.io"
        introductionPage = "/Coalesce/introduction.html"
        url = siteUrl + introductionPage

        try:
            links = endpoints._scrape_nav_links_from_site(url)
            pages = []

            for link in links:
                text = endpoints._scrape_text_from_site(siteUrl + link)
                pages.append(
                    {"id": f"{siteUrl}{link}", "metadata": {"source": link}, "document": text}
                )

            if pages:
                endpoints._persist_document_collection(pages)
                return 200
            else:
                return "Failed to scrape text from the provided URL.", 400
        except Exception as e:
            return "Error:", e, 400

    # Private Helpers
    @staticmethod
    def _scrape_text_from_site(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "html.parser")

            # Find and collect text from all paragraphs on the page
            content_sections = soup.find(class_="content-container")
            content = content_sections.find_all(
                [
                    "p",
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "ul",
                    "ol",
                    "li",
                    "a",
                    "table",
                    "tr",
                    "td",
                ]
            )
            text = " ".join([c.get_text() for c in content])

            return text
        else:
            return ""

    @staticmethod
    def _scrape_nav_links_from_site(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, "html.parser")

            # Find and collect nav links from the nav bar
            navbar = soup.find(id="VPSidebarNav")
            links = navbar.find_all("a")

            hrefs = [link.get("href") for link in links]
            return hrefs
        else:
            return []

    @staticmethod
    def _persist_document_collection(pages):
        chroma_client = chromadb.PersistentClient(path="persist")
        try:
            collection = chroma_client.get_collection(endpoints.collection_name)
        except ValueError:
            print("Running first time collection setup...")
            collection = chroma_client.create_collection(name="coalesce_docs")
        documents = [page["document"] for page in pages]
        metadatas = [page["metadata"] for page in pages]
        ids = [page["id"] for page in pages]

        print('Persisting documents...')
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print('Finished persisting.')

    @staticmethod
    def _delete_document_collection():
        chroma_client = chromadb.PersistentClient(path="persist")
        try:
            chroma_client.get_collection(endpoints.collection_name)
            chroma_client.delete_collection(endpoints.collection_name)
        except ValueError:
            print("Collection does not exist!")

# endregion