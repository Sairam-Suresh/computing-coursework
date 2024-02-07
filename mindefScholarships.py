#Done By: Ayaan

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


def mindefScholarship():
    link = "https://www.mindef.gov.sg/oms/scholarship/"
    website = requests.get(link)

    soup = BeautifulSoup(website.content, "html.parser")

    results = soup.find_all("a", class_="banner-findout")
    
    scholarship_links = []
    scholarship_results = []

    for result in results:
        #print(result)
        result = str(result)
        start = result.find("scholarships")
        end = result.find(" id=")
        scholarship_links.append(result[start:end-1])


    for scholarship in scholarship_links:
        scholarship_link = "https://www.mindef.gov.sg/oms/scholarship/"+scholarship
        website_scholarship = requests.get(scholarship_link)
        
        soup_scholarship = BeautifulSoup(website_scholarship.content, "html.parser")


        scholarship_body = soup_scholarship.get_text()

        #scholarship_results.append([scholarship_link, scholarship_body[eligibility_criteria_index:value_award_index].replace("\n", ""), scholarship_body[value_award_index:courses_index].replace("\n", ""), scholarship_body[courses_index:goal_universities_index].replace("\n", ""), scholarship_body[goal_universities_index:ending_index].replace("\n", "")])
        scholarship_results.append([scholarship_link, scholarship_body.replace("\n", "")])


    return scholarship_results
