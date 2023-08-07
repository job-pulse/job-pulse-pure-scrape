import openai
import logging
from models import JobCategory, ExperienceCategory
from dotenv import load_dotenv
import os


load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
NUMBER_PRINTER = "You are a helpful number printer that print a number and the number only"
YES_NO_PRINTER = "You are a helpful yes/no printer that print 'yes' or 'no' and the word only"

def ask_gpt(input_ask, role):  
    
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": role},
        {"role": "user", "content": input_ask}
    ]
    )

    res = completion.choices[0].message.content

    # if it is string, return lower case, strip the space and .
    if isinstance(res, str):
        res = res.lower()
        res = res.strip()
        res = res.strip(".")
    return res


def gpt_get_yoe_from_jd(JDText):

    yoe_requirement = None
    ask_yoe = "What's the minimum number of work experience for this job? Here is the job description\n" + '"""' + JDText + '"""\n' + "You MUST say a number and SAY THE THE NUMBER ONLY. If there is no number mentioned in the text, print '0' and '0' only.\n The number is "
    yoe_requirement = ask_gpt(ask_yoe, NUMBER_PRINTER)
    # if the string can be converted to int, return int
    # other wise return -1
    try:
        yoe_requirement = int(yoe_requirement)
    except:
        yoe_requirement = -1
        
    return yoe_requirement


def gpt_check_job_title(job_title, job_category, experience_category=None, yoe=None):
    try:
        # set the experience category string
        intern_extra_keyword = ""
        ng_extra_keyword = ""
        if experience_category and experience_category==ExperienceCategory.Intern:
            intern_extra_keyword = "internship "
        elif yoe and isinstance(yoe, int) and yoe < 2:
            ng_extra_keyword = "entry level "

        if job_category==JobCategory.Software_Engineer:
            question = f"Given the job title '{job_title}', does it look like a {ng_extra_keyword}software engineering or IT related {intern_extra_keyword}role? Answer 'yes' or 'no' with no punctuation."
        elif job_category==JobCategory.Product_Manager:
            question = f"Given the job title '{job_title}', does it look like a product manager related role? Answer 'yes' or 'no' with no punctuation." # don't apply to PM because GPT thinks PM is always senior

        gpt_answer = ask_gpt(question, YES_NO_PRINTER)
        if "yes" in gpt_answer.lower():
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error in gpt_check_job_title: {e}, returning True to be safe")
        return True
    