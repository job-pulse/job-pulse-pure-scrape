

import logging 

class MockFirebaseHandler:
    def __init__(self):        
        pass

    def add_job(self, job_data, db_collection_name):
        logging.info(f"(mock) Adding job to {db_collection_name} collection: {str(job_data)[:10]}...")

