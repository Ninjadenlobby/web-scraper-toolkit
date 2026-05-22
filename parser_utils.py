from urllib.parse import urljoin

from bs4 import BeautifulSoup


def extract_meta(soup: BeautifulSoup) -> dict:
    """Extract title and meta description from a page."""
    title = soup.title.string.strip() if soup.title and soup.title.string else None

    description = None
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()

    return {"title": title, "description": description}


def extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Extract all href links from the page."""
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full_url = urljoin(base_url, href)
        if full_url.startswith("http"):
            links.append(full_url)
    return sorted(set(links))
