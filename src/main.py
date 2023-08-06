import argparse
from pure_scrape.pure_scrape_runner import run_pure_scrape

# python3 src/main.py --run_pure

def main(run_pure=False):
    if run_pure:
        run_pure_scrape()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to control the running of the various scrapers")
    parser.add_argument("--run_pure", action="store_true", help="Run pure scrape")

    args = parser.parse_args()
    main(args.run_pure)

