
from datetime import datetime
from util.logger import setup_logging
from .apple import AppleJobsScraper
from .netflix import NetflixJobsScraper
from .meta import MetaJobsScraper




def run_pure_scrape(prod=False):
    setup_logging(f"logs/pure_scrape_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log")
    meta_scraper = MetaJobsScraper(site="https://www.metacareers.com/jobs/", query="software engineer")
    netflix_scraper = NetflixJobsScraper(site="https://jobs.netflix.com/jobs/", query="software engineer")
    apple_scraper = AppleJobsScraper(site="https://jobs.apple.com/en-us/details/", query="software engineer")

    meta_scraper.scrape_jobs()
    netflix_scraper.scrape_jobs()
    apple_scraper.scrape_jobs()

if __name__ == "__main__":
    run_pure_scrape()



