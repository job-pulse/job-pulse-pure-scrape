from datetime import datetime
from .pure_scraper import PureScraper

class AppleJobsScraper(PureScraper):
    company_name = 'Apple'

    def get_job_title(self, soup):
        title_tag = soup.find('h1', id='jdPostingTitle')
        return title_tag.text.strip() if title_tag else None

    def get_key_qualification(self, soup):
        qual_tag = soup.find('div', id='jd-key-qualifications')
        edu_exp_tag = soup.find('div', id='jd-education-experience')
        texts = []
        if qual_tag:
            texts.append(qual_tag.text.strip())
        if edu_exp_tag:
            texts.append(edu_exp_tag.text.strip())
        return ' '.join(texts) if texts else None

    def get_country_text(self, soup):
        country_tag = soup.find('span', itemprop='addressCountry')
        return country_tag.text.strip() if country_tag else None

    def get_post_time(self, soup, snippet):
        time_tag = soup.find('time', id='jobPostDate')
        if time_tag and 'datetime' in time_tag.attrs:
            post_time_str = time_tag['datetime']
            post_time = datetime.strptime(post_time_str, '%Y-%m-%d')
            return post_time
        return None