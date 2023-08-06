from datetime import datetime, timedelta
from .pure_scraper import PureScraper
import re

class MetaJobsScraper(PureScraper):
    company_name = 'Facebook'

    def get_job_title(self, soup):
        div_tag = soup.find('div', class_="_9ata _8ww0")
        return div_tag.text.strip() if div_tag else None

    def get_key_qualification(self, soup):
        qual_tags = soup.find_all('div', class_="_8muv")
        qualifications = []
        for tag in qual_tags:
            qualifications.append(tag.text.strip())

        return ' '.join(qualifications)

    def get_country_text(self, soup):
        span_tag = soup.find('span', class_="_8lfp _9a80 _97fe")
        return span_tag.text.strip() if span_tag else None
    
    def get_post_time(self, soup, snippet):
        # Regular expression pattern to find 'x day(s) ago' or 'x hour(s) ago' in the snippet
        pattern_days = r'(\d+)\sday[s]? ago'
        pattern_hours = r'(\d+)\shour[s]? ago'

        match_days = re.search(pattern_days, snippet)
        match_hours = re.search(pattern_hours, snippet)

        # If the pattern is found, subtract the number of days or hours from the current date
        if match_days:
            days_ago = int(match_days.group(1))
            post_time = datetime.now() - timedelta(days=days_ago)
        elif match_hours:
            hours_ago = int(match_hours.group(1))
            post_time = datetime.now() - timedelta(hours=hours_ago)
        else:
            # Default to current date if no match is found
            post_time = datetime.now()

        # Format the date as a string in the format '%Y-%m-%d %H:%M:%S'
        post_time_str = post_time.strftime('%Y-%m-%d %H:%M:%S')
        post_time = datetime.strptime(post_time_str, '%Y-%m-%d %H:%M:%S')
        # print(post_time, type(post_time))
        return post_time
