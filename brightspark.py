# This script was created in full by Lohith Ishan from S401
# Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import re
import time

def brightsparks():
    # website being used to search scholarships
    url = 'https://brightsparks.com.sg/searchScholarships.php'
    start = time.time()

    # Opening Website
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Exit the ad if it appears
    driver.find_element(By.CLASS_NAME, "close").click()

    # Select dropdown to choose scholarships based on university students
    Select(driver.find_element(By.ID, "eligibility")).select_by_value("4")
    driver.find_element(By.CLASS_NAME, "btn-ss").click()

    # Keeps clicking the show-more button to show all the scholarships
    while True:
        try:
            try:
                driver.find_element(By.CLASS_NAME, "close").click()
            except:
                search = driver.find_element(By.ID, "details")
                search.find_element(By.CLASS_NAME, "show-more").click()
        except:
            break

    # Function to scrape a website and find all scholarships within
    def websitescraper(link):

        # Setup scholarship website
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless=new")
        opt.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ""AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
        drive = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=opt)
        drive.get(link)

        # Links that are paired with the content will be in this list
        paired_links = []

        # Variables
        save = drive.current_url
        possible_hrefs = ['//a[@href="scholarship.php"]', '//a[@href="scholarships.php"]', '//a[@href="scholar.php"]',
                          '//a[@href="mpa-scholarship-programme.php"]', '//a[@href="ss-scholarship.php"]', '//a[@href="uni.php"]',
                          '//a[@href="midterm.php?schid=10441"]', '//area[@href="scholarship.php"]','//a[@href="phd.php"]',
                          '//a[@href="scholarships_bcaundergrad.php"]', '//a[@href="csit-undergraduate-scholarship.php"]',
                          '//a[@href="our-scholarships.php"]',"scholarship-available.php", '//a[@href="#"]']


        print(save)
        try:
            if "aic" in save:
                return paired_links
            print([a.get_attribute("href") for a in drive.find_elements(By.CSS_SELECTOR, "a") if
                   (("view" in a.get_attribute("href") or "php" in a.get_attribute("href")) and "dukenus" in save) or ("view" in (a.get_attribute("href") and "php" in a.get_attribute("href")))])
            if [a.get_attribute("href") for a in drive.find_elements(By.CSS_SELECTOR, "a") if
                "view" in a.get_attribute("href") or "php" in a.get_attribute("href")]:
                print("It is Inside")

                # This checks if the content in the current link already has the information
                for i in [a.get_attribute("href") for a in drive.find_elements(By.CSS_SELECTOR, "a") if
                          "view" in a.get_attribute("href") or "php" in a.get_attribute("href")]:
                    drive.quit()
                    openlink = requests.get(i)
                    opensoup = BeautifulSoup(openlink.content, 'html.parser')
                    paired_links.append([openlink.url, re.sub(r"\n+", "\n", "".join(
                        [i.text for i in opensoup.find("div", class_="scholarship_description")] if opensoup.find("div", class_="scholarship_description") is not None and "dukenus" in save else [i.text for i in opensoup.find_all("p")]))])
                print("It is in First Loop")
                return paired_links if "dukenus" not in save else paired_links[4:-1]

            # For certain websites, this code will take the information from the first page
            if "SNS" not in save and "dsg" not in save:
                soup = BeautifulSoup(drive.page_source, 'html.parser')
                try:
                    paired_links.append([save, re.sub(r"\n+", "\n", "".join([i.text for i in soup.find("div", class_="col-md-12")]))])
                    drive.quit()
                    print('It Has Worked Out')
                    return paired_links
                except:
                    raise NoSuchElementException
        except:
            # If the websites do not fall under the previous criteria, they will end up here
            # This code checks if it can navigate to the area where the code will be found.
            print('Second Loop')
            navbaropen = False
            for i in possible_hrefs:
                if not navbaropen:
                    try:
                        try:
                            drive.find_element(By.CLASS_NAME, "navbar-toggle").click()
                        except:
                            drive.find_element(By.CLASS_NAME, "navbar-toggler").click()
                        navbaropen = True
                    except:
                        navbaropen = False
                try:
                    if "astar" in save and "scholarship" in i:
                        continue
                    drive.find_element(By.XPATH, i).click()
                    break
                except:
                    if i == possible_hrefs[-1]:
                        print("It is Here")
                        if "nuhs" in save:
                            drive.find_element(By.XPATH, '//a[@href="index.php"]').click()
                            print("It has Broken")
                            break
                        drive.quit()
                        print("Unique Identifier")
                        return ""


        # Wait for the code to load and opens new link
        time.sleep(5)
        soup = BeautifulSoup(drive.page_source, 'html.parser')
        save = drive.current_url
        print('Second Check')
        print(save)
        drive.quit()

        # This checks if there are any links related to scholarships within the current website
        linklist = [a["href"] for a in soup.find_all('a', href=True) if "http" in a["href"] and "brightsparks" in a["href"] and a["href"]!= "https://brightsparks.com.sg/"]
        print(linklist)

        # If there are no links in the current website, It will get information from the current website
        # Else it will loop through the links in the website for each scholarship
        if not linklist:
            try:
                if soup.find("div",id="collapseOne") is None:
                    desc = "".join([i.getText() for i in soup.find("div", id="scholarship_description")])
                elif soup.find("div",id="inner-banner") is None:
                    desc = "".join([i.getText() for i in soup.find("div", class_="inner-banner")])
                elif soup.find("figure",class_="tabBlock"):
                    print([i for i in soup.find("figure", class_="tabBlock")])
                    desc = "".join([i.getText() for i in soup.find("figure", class_="tabBlock")])
                    print(desc)
                paired_links.append([save, re.sub(r"\n+", "\n", desc)])
            except:
                print("Unable to Find")
                return ""
        else:
            try:
                print(linklist)
                for i in range(len(linklist)):
                    openlink = requests.get(linklist[i])
                    opensoup = BeautifulSoup(openlink.content, 'html.parser')
                    paired_links.append([openlink.url, re.sub(r"\n+", "\n", "".join([i.getText() for i in opensoup.find("div", id="scholarship_description")] if opensoup.find("div", id="collapseOne") is None else [i.getText() for i in opensoup.find("div", id="collapseOne")] if opensoup.find("div", id="wrapper") is None else [i.getText() for i in opensoup.find("div", id="scholarship_description")] if opensoup.find("div", id="collapseOne") is None else [i.getText() for i in opensoup.find("div", id="collapseOne")]))])
            except:
                print("" ,end="")
                print("Something went Wrong")
        return paired_links


    # Get all the scholarships
    elements = driver.find_elements(By.CLASS_NAME, 'col-span-11')


    # Extracts scholarships from the list of websites
    sitelist = []
    information = []
    for title in range(len(elements)):
        heading = elements[title].find_element(By.ID, "getUpdatedTitle").text
        elem = elements[title].find_element(By.TAG_NAME, "a")
        site = elem.get_attribute('href').split("(")[0]
        if site not in sitelist:
            sitelist.append(site)
            information += websitescraper(site)
    return [i for i in information if type(i) == type([])]