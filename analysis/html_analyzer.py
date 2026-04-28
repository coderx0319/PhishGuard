from bs4 import BeautifulSoup
import tldextract

def get_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def analyze_html(body):
    soup = BeautifulSoup(body, "html.parser")

    suspicious = []

    for link in soup.find_all("a"):
        href = link.get("href")
        text = link.text.strip()

        if not href:
            continue

        href_domain = get_domain(href)

        # Extract domain from visible text if it's a URL
        text_domain = None
        if "http" in text:
            try:
                text_domain = get_domain(text)
            except:
                pass

        # 🚨 Detection logic
        if text_domain and href_domain != text_domain:
            suspicious.append({
                "text": text,
                "href": href,
                "text_domain": text_domain,
                "actual_domain": href_domain,
                "reason": "Displayed URL domain does not match actual link domain"
            })

    return suspicious