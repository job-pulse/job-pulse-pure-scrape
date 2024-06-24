# [NOTICE] This repo is deprecated. Open sourcing it didn't work.

<del>
# JobPulse.fyi Open Source Web Scraper

[JobPulse.fyi](https://jobpulse.fyi/?utm_source=github) is a powerful tool that tracks software engineering and product manager openings tailored for students. This repository is a part of the JobPulse.fyi project and is designed to scrape job information from company websites using Google's API.

## Features

- **Job search:** Given a query and a website, the scraper searches for job listings that match the query.
- **Data extraction:** The scraper visits each job listing page and extracts relevant data, such as job title, years of experience, company, application link, location, and job description.

## Getting Started

### Prerequisites

- Python 3.7 or above
- Packages: BeautifulSoup, selenium, pytz, requests
- Google API key
- OpenAI API key

### Installation

1. Clone this repository:


2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Get a Google API Key:

   - Follow the steps from [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/introduction) to obtain a Google API key and a Search Engine ID (cx key).

4. Get an OpenAI API Key:

   - Follow the steps from [OpenAI](https://beta.openai.com/docs/developer-quickstart/) to get an API key.

5. Set the environment variables:

   - Copy the `.env.example` file to a new file named `.env` and fill in the appropriate keys:

        ```bash
        GOOGLE_API_KEY=your_google_api_key
        CX_KEY=your_cx_key
        OPENAI_KEY=your_openai_key
        ```

### Usage

1. Modify the query and site variables in the `main` function as per your requirements.
2. Run the code:

    ```bash
    python3 src/main.py --run_pure
    ```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Please feel free to contact us if you have any questions about the project.

Join us on Discord: [Discord Link](https://discord.gg/R6rWBFhzF2)


Happy Coding!

*This README is subject to updates, please stay tuned for any changes.*

jobPosting schema class
   Mandatory:
   - apply_link: str
   - company: str
   - date_added: str
   - title: str

   Optional:
   - description: str
   - location: str
   - category: "Software Engineer"
   - title_correct_by_gpt: True

</del>
