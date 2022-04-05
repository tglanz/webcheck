import logging
import requests
import webcheck

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s [%(levelname)s] %(message)s")

def main():
    urls = (
        'https://www.ynet.com',
        'https://www.google.com',
        'https://www.bing.com')

    for url in urls:
        response = requests.get(url)
        print(f"Status code returned from {url}: {response.status_code}")

if __name__ == '__main__':
    setup_logging()
    main()
