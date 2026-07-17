import urllib.request
from bs4 import BeautifulSoup
from syntex.core.logger import logger

class DocScraper:
    def __init__(self):
        # initialize the documentation scraper
        pass

    def scrape_url(self, url: str) -> str:
        # fetch html content from the provided url
        try:
            logger.info(f"scraping documentation from: {url}")
            
            # use a standard user-agent to bypass basic bot blockers
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req) as response:
                html_content = response.read()

            # parse html and remove noisy web elements
            soup = BeautifulSoup(html_content, "html.parser")
            
            # strip out scripts, styles, headers, and footers
            for noisy_element in soup(["script", "style", "nav", "footer", "header"]):
                noisy_element.extract()
                
            # extract text and clean up excess whitespace
            text = soup.get_text(separator="\n")
            clean_text = "\n".join(
                line.strip() for line in text.splitlines() if line.strip()
            )
            
            return clean_text

        except Exception as e:
            logger.error(f"failed to scrape {url}: {e}")
            return ""
