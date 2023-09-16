import sys
sys.path.append('../') 

from util.repoUtils.getGitRepoPostings import fetch_and_save_data
from util.firebase_handler import FirebaseHandler

from util.repoUtils.gitConstants import ng_us_urls, intern_us_urls, \
  ng_us_output_filename, intern_us_output_filename

ng_us_postings = fetch_and_save_data(ng_us_urls, ng_us_output_filename, "USA")
intern_us_postings = fetch_and_save_data(intern_us_urls, intern_us_output_filename, "USA")


firebase_handler = FirebaseHandler()

for data in ng_us_postings:
    firebase_handler.add_job(data, 'all_companies')

for data in intern_us_postings:
    firebase_handler.add_job(data, 'all_companies') 