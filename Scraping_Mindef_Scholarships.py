# This script was created in full by Ayaan Jain from S408

# Website scraped by this programme: https://www.mindef.gov.sg/oms/scholarship/

# Imports
from bs4 import BeautifulSoup
import requests


def mindef_scholarships():
    link = "https://www.mindef.gov.sg/oms/scholarship/"
    website = requests.get(link)

    soup = BeautifulSoup(website.content, "html.parser")

    # Find all banners on the website
    results = soup.find_all("a", class_="banner-findout")
    
    scholarship_links = []
    scholarship_results = []

    # Gather all the different scholarships and place the link to their individual pages in a list
    for result in results:
        result = str(result)
        start = result.find("scholarships")
        end = result.find(" id=")
        scholarship_links.append(result[start:end-1])

    # Scrape the individual pages of each scholarship (medicine and dentistry are not scraped as it is not supported in the website and therefore not considered)
    for scholarship in scholarship_links:
        scholarship_link = "https://www.mindef.gov.sg/oms/scholarship/"+scholarship
        website_scholarship = requests.get(scholarship_link)
        
        soup_scholarship = BeautifulSoup(website_scholarship.content, "html.parser")

        scholarship_body = soup_scholarship.get_text()

        scholarship_results.append([scholarship_link, scholarship_body.replace("\n", "")])


    return scholarship_results