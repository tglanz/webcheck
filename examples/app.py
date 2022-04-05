import argparse
import logging
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level",
        type=str, default="info", choices=["debug", "info", "warning", "error"])
    parser.add_argument("--url", type=str, default="http://www.google.com")
    parser.add_argument("--webcheck", action="store_const", const=True)
    return parser.parse_args()

def setup_logging(log_level: str):
    logging.basicConfig(
        level=logging.getLevelName(log_level.upper()),
        format="%(asctime)s - %(name)s [%(levelname)s] %(message)s")

def main(url: str):
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")

if __name__ == '__main__':
    args = parse_args()
    setup_logging(args.log_level)

    if args.webcheck:
        import webcheck

    main(args.url)
