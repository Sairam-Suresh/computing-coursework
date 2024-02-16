# This script was created in full by Ayaan Jain from S408

# Website scraped by this program:
# https://www.scholars4dev.com/10017/top-100-international-scholarships-international-students/

# Imports
from bs4 import BeautifulSoup
import requests


def Scholars4Dev():
    link = "https://www.scholars4dev.com/10017/top-100-international-scholarships-international-students/"
    website = requests.get(link)

    soup = BeautifulSoup(website.content, "html.parser")

    # Find all banners on the website
    results = soup.find_all("a", href=True)
    
    scholarship_links = []
    scholarship_results = []

    # Gather all the different scholarships and place the link to their individual pages in a list
    for result in results:
        result = str(result)
        start = result.find("https://www.scholars4dev.com/")
        end = result.find('">')
        scholarship_links.append(result[start:end-1])

    # Scrape the individual pages of each scholarship (medicine and dentistry are not scraped as it is not supported
    # in the website and therefore not considered)
    for i in range(4, len(scholarship_links)):
        scholarship_link = scholarship_links[i]
        if scholarship_link:
            website_scholarship = requests.get(scholarship_link)
        
            soup_scholarship = BeautifulSoup(website_scholarship.content, "html.parser")

            scholarship_body = soup_scholarship.get_text()

            scholarship_results.append([scholarship_link, scholarship_body.replace("\n", "")])

    return scholarship_results

print(Scholars4Dev())
