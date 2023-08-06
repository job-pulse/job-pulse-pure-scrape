from datetime import datetime
from .pure_scraper import PureScraper
import pytz

class NetflixJobsScraper(PureScraper):
    company_name = 'Netflix'

    def get_job_title(self, soup):
        title_tag = soup.find('h1')
        return title_tag.text.strip() if title_tag else None

    def get_key_qualification(self, soup):
        div_tag = soup.find('div', class_='css-9x8k7t e1spn5rx7')
        return ' '.join(div_tag.stripped_strings) if div_tag else None

    def get_country_text(self, soup):
        country_tag = soup.find('span', class_='css-ipl420 e13jx43x2')
        return country_tag.text.strip() if country_tag else None
    
    def get_post_time(self, soup, snippet):
        # return current time
        return datetime.now(tz=pytz.utc)