from pathlib import Path
from flask import request
import requests
import bs4

class endpoints: 
# region Chat Endpoint
    @staticmethod
    def chat(chain):
        data = request.get_json()
        query = data["message"]
        chat_history = data = [tuple(item) for item in data["chat_history"]]

        result = chain({"question": query, "chat_history": chat_history})

        chat_history.append((query, result['answer']))

        # Only save the last 10 messages, since we are doing this all in memory
        response = {"chat_history": chat_history[-10:]}
        query = None

        return response
#endregion

#region Scrape Endpoint
    @staticmethod
    def scrape():
        siteUrl = 'https://intellitect.github.io'
        introductionPage = '/Coalesce/introduction.html'
        url = siteUrl + introductionPage

        try:
            links = endpoints._scrape_nav_links_from_site(url)
            text = ''

            for link in links:
                text += endpoints._scrape_text_from_site(siteUrl + link)

            if text:
                endpoints._save_text_to_file(text)
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
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            # Find and collect text from all paragraphs on the page
            content_sections = soup.find(class_='content-container')
            content = content_sections.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a', 'table', 'tr', 'td'])
            text = ' '.join([c.get_text() for c in content])

            return text
        else:
            return ''
        
    @staticmethod
    def _scrape_nav_links_from_site(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            # Find and collect nav links from the nav bar
            navbar = soup.find(id='VPSidebarNav')
            links = navbar.find_all('a')

            hrefs = [link.get('href') for link in links]
            return hrefs
        else:
            return []
        
    @staticmethod
    def _save_text_to_file(text):
        script_directory = Path(__file__).parent
        file_path = script_directory / 'data' / 'docs.txt'
        
        with open(file_path, 'w', encoding='utf-8') as file:
            print(f'writing {len(text)} characters to  {file_path}... Be patient')
            file.write(text)
            print('done writing')
#endregion