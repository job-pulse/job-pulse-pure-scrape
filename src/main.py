import argparse
from pure_scrape.pure_scrape_runner import run_pure_scrape
from github_scrape.git_scraper import run_git_scrape

# python3 src/main.py --run_pure

def main(run_pure, prod, run_git):
    if run_pure:
        run_pure_scrape(prod=prod)
    if run_git:
        run_git_scrape()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to control the running of the various scrapers")
    parser.add_argument("--run_pure", action="store_true", help="Run pure scrape")
    parser.add_argument("--prod", action="store_true", help="Run pure scrape")
    parser.add_argument("--run_git", action="store_true", help="Run git scrape")


    args = parser.parse_args()
    main(args.run_pure, args.prod, args.run_git)

