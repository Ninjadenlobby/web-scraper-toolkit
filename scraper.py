import argparse
import json
import time

import requests
from bs4 import BeautifulSoup

from parser_utils import extract_meta, extract_links


def fetch_page(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": "web-scraper-toolkit/1.0"}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def scrape(url: str, get_links: bool = False) -> dict:
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")

    result = {"url": url, **extract_meta(soup)}

    if get_links:
        result["links"] = extract_links(soup, url)

    return result


def main():
    parser = argparse.ArgumentParser(description="Scrape web pages for metadata and links")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--links", action="store_true", help="Extract all links")
    parser.add_argument("--output", "-o", help="Save results to JSON file")
    parser.add_argument("--delay", type=float, default=0, help="Delay between requests (seconds)")

    args = parser.parse_args()

    if args.delay > 0:
        time.sleep(args.delay)

    result = scrape(args.url, get_links=args.links)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
