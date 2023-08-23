
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from .country import standardize_country
import pytz
from util.GPTInterface import gpt_check_job_title, gpt_get_yoe_from_jd
from .google_api import filter_links, search_jobs
from datetime import datetime
from abc import ABC, abstractmethod
from models import JobCategory, ExperienceCategory
import logging
import platform

def display_data(data):
    logging.info("----------------")
    logging.info(f"Title: {data.get('title')}")
    logging.info(f"Post Time: {data.get('date_added')}")
    logging.info(f"title check: {data.get('title_correct_by_gpt')}")
    logging.info(f"Years of Experience: {data.get('yoe')}")
    logging.info(f"Company: {data.get('company')}")
    logging.info(f"Apply Link: {data.get('apply_link')}")
    logging.info(f"Location: {data.get('location')}")

    # get the first 10 words from the description
    description = data.get('description')
    if description:
        words = description.split()
        logging.info("Description (first 10 words): %s", ' '.join(words[:10]))

class PureScraper(ABC):
    def __init__(self, site, query, num_results=10, day=1, prod=False):
        self.site = site
        self.query = query
        self.num_results = num_results
        self.day = day
        if prod:
            from util.firebase_handler import FirebaseHandler
            self.db_handler = FirebaseHandler()
        else:
            from util.mock_firebase_handler import MockFirebaseHandler
            self.db_handler = MockFirebaseHandler()

        # set up driver (It's stupid to upload the driver to github, but this is convenient for now)
        system = platform.system()
        if system == "Linux":
            logging.info("----------Linux------")

            self.chrome_executable_path = "./chromedriver_linux"
        elif system == "Darwin":  # MacOS is recognized as 'Darwin' by platform.system()
            logging.info("----------MAC------")
            
            self.chrome_executable_path = "./chromedriver"
        elif system == "Windows":  # MacOS is recognized as 'Darwin' by platform.system()
            logging.info("----------Windows------")
            self.chrome_executable_path = "./chromedriver.exe"

        else:
            raise Exception(f"Unsupported OS: {system}")
   
    @property
    @abstractmethod
    def company_name(self):
        """mandatory: The name of the company that the scraper is scraping for"""
        pass

    def get_job_title(self, soup):
        raise NotImplementedError

    def get_key_qualification(self, soup):
        raise NotImplementedError

    def get_country_text(self, soup):
        raise NotImplementedError

    def get_post_time(self, soup, snippet):
        raise NotImplementedError

    def scrape_job_page(self, driver, url, snippet, IsIntern=False):
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # get the job title, job description, location, post time from the job page
        job_title = self.get_job_title(soup)
        job_des = self.get_key_qualification(soup)
        location = self.get_country_text(soup)
        location = standardize_country(location)
        post_time = self.get_post_time(soup, snippet)
        post_time_unix = datetime.now(tz=pytz.utc) if post_time is None else post_time

        # get the years of experience from the job description
        yoe = "intern"
        if not IsIntern and job_des:
            yoe = gpt_get_yoe_from_jd(job_des)
        
        # check if the job title is relevant to the query
        if not IsIntern:
            experience_category = ExperienceCategory.Full_Time
        else:
            experience_category = ExperienceCategory.Intern
        # hard code yoe so that we force the entry level check. Jobs found on google are sometimes ridiculously high yoe
        job_title_correct = gpt_check_job_title(job_title, self.current_job_category, experience_category=experience_category, yoe=1) 

        return {
            'title': job_title,
            'yoe': yoe,
            'company': self.company_name,
            'apply_link': url,
            'location': location,
            'description': job_des,
            "title_correct_by_gpt": job_title_correct,
            'category': "Software Engineer", #TODO this should be a parameter
            "date_added": post_time_unix,
            "pure_scrape": True,
        } if (job_title and location) else None

    def scrape_jobs(self):
        # get the job listings from google search
        job_listings = search_jobs(self.query, self.site, num_results=self.num_results, day=self.day)
        grad_job_listings, intern_job_listing = filter_links(job_listings)

        # init driver
        options = Options()
        options.add_argument("--headless") # Ensure GUI is off. Remove if you want to see the browser.
        # driver = webdriver.Chrome(executable_path=self.chrome_executable_path, options=options)
        service = Service(self.chrome_executable_path)
        driver = webdriver.Chrome(service=service, options=options)
        if "software" in self.query.lower():
            self.current_job_category = JobCategory.Software_Engineer
        else:   
            logging.warning("Job category not found, defaulting to software engineer")
            raise NotImplementedError
        

        # scrape the job pages
        for job in grad_job_listings:
            data = self.scrape_job_page(driver, job['link'], job['snippet'])
            if data:
                display_data(data)
                # transformed_data = build_job_data(data) # TODO this can be deleted now, already taken care of
                self.db_handler.add_job(data, 'linkedin_jobs')

        for job in intern_job_listing:
            data = self.scrape_job_page(driver, job['link'], job['snippet'], IsIntern=True)
            if data:
                display_data(data)
                # transformed_data = build_job_data(data) # TODO this can be deleted now, already taken care of
                self.db_handler.add_job(data, 'linkedin_jobs')


        driver.quit()







