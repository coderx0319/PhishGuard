import re
from bs4 import BeautifulSoup

URL_REGEX = r'https?://[^\s<>"\']+'
IP_REGEX = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

def extract_iocs(text):
    urls = set()
    ips = set()

    # Regex extraction
    urls.update(re.findall(URL_REGEX, text))
    ips.update(re.findall(IP_REGEX, text))

    # HTML extraction (IMPORTANT)
    try:
        soup = BeautifulSoup(text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                urls.add(href)
    except:
        pass

    return {
        "urls": list(urls),
        "ips": list(ips)
    }