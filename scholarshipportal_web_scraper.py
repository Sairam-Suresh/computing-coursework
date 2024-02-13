# This script was created in full by Sairam Suresh from S401

# Imports
import itertools
import multiprocessing
import pickle
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time
import re
from threading import Timer


# Function to scrape necessary data from the detail view of the scholarship
# link.
def scrape_scholarship_details(url, selenium_lock: multiprocessing.Lock):
    sleep_time = 4

    # Warm up the selenium instance
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    )
    opts.add_argument("--disable-gpu")
    web_driver = webdriver.Chrome(options=opts)
    web_driver.delete_all_cookies()

    try:
        # Acquire the lock to prevent other processes from accessing the website at the same time
        selenium_lock.acquire()
        web_driver.get(url)

        detailed_soup = BeautifulSoup(web_driver.page_source, "html.parser")

        # Dispose of the web browser as soon as we possibly can to free resources
        web_driver.close()
        web_driver.quit()

        # Parse the the details using BeautifulSoup
        details = "\n".join([desc.text for desc in detailed_soup.find_all("div", class_="content")])

        # Sleep for a bit first before releasing lock to prevent a website overload while also
        # not blocking this process. We add an extra delay to the release to the lock just in
        # case we try scraping too fast
        Timer(sleep_time + (1.5 if (details == '') else 0), selenium_lock.release).start()

        print("Scraped: " + url)

        # Return the result
        return [url, details]
    except Exception as e:
        # For some reason some pages fail to load, so we just ignore them since it would not affect the overall result
        # too much
        print(f"Non-severe warning: Error parsing data from {url}: {e}."
              f" Continuing anyway.")
        try:
            # Dispose all resources after exception
            web_driver.close()
            web_driver.quit()
            selenium_lock.release()
        except ValueError:
            # This means that the lock is already released
            # So we continue anyway
            pass
        return None


def scrape_scholarship_urls(driver):
    # This portion scrapes all the scholarship links from the main page(s), by
    # using a while loop to go to the next page using the URL itself until we hit
    # a 404, which would mean that there are no more scholarships to scrape
    page_index = 1
    all_scholarship_links = []
    while True:
        driver.delete_all_cookies()
        driver.get(f"https://www.scholarshipportal.com/scholarships/singapore?page={page_index}")
        sleep(7)

        # Scroll to the bottom of the page to load all scholarships
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all "a" tags with a href attribute that contains "/scholarship/" in it, which is the scholarship's
        # detail page
        scholarship_links_on_page = soup.find_all("a", href=re.compile(r"/scholarship/"))

        if len(scholarship_links_on_page) != 0:
            # This only executes when the scraper detects that there are scholarships on the page in question
            for i in scholarship_links_on_page:
                all_scholarship_links.append("https://www.scholarshipportal.com"+i.get("href"))
            page_index += 1
        else:
            # If no more scholarships are found, it means we probably hit a 404, which would mean that
            # There are no more scholarships left to scrape. Therefore break the loop
            break

    return all_scholarship_links


def scrape_all_scholarships_details(scholarship_links: list):
    scholarships = []

    # Create a Manager and obtain a lock for usage in the scrape_scholarship_details function
    m = multiprocessing.Manager()
    lock = m.Lock()

    # This part uses a Process pool to scrape all the scholarships in parallel, reducing
    # The time taken to scrape the websites
    print("Starting...")

    try:
        with ProcessPoolExecutor(max_workers=5) as executor:
            for i in executor.map(scrape_scholarship_details, scholarship_links, itertools.repeat(lock)):
                scholarships.append(i)
    except pickle.PicklingError:
        # This means that something somehow went wrong, but since it does not destroy any data we just continue
        print("Scraper has stopped scraping due to an error. Continuing with preexisting data.")
        pass

    print("Ended...")

    # Filter out all the scholarships that could not be scraped
    filtered_scholarships = list(filter((lambda x: x is not None and x[1] != ""), scholarships))
    return filtered_scholarships


def scrape():
    # This part of code can be shared between running the script as a standalone script or as a module
    is_main = __name__ == "__main__"
    start_time = time()

    # Warm up the Selenium instance
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    )
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()

    # Scrape the scholarship links
    scholarship_links = scrape_scholarship_urls(driver)

    # Free resources
    driver.close()
    driver.quit()

    # This portion scrapes the details of all the scholarships by navigating to each URL
    scholarships = scrape_all_scholarships_details(scholarship_links)

    if is_main:
        # If this script is being run as a standalone script, then we should give
        # debug information and print stats to console
        print(len(scholarship_links))
        print(f"Time taken: {(time() - start_time)/60} minutes")
        print(f"Total successful scraped scholarships / Total Scholarships:"
              f" {len(scholarships)} / {len(scholarship_links)}")
        print(f"Percentage of successful scraped scholarships:"
              f" {(len(scholarships) / len(scholarship_links)) * 100}%")
        print(f"Average time taken per successful website: {(time() - start_time) / len(scholarships)} seconds")

    return scholarships


# If we are running this as main, automatically assume that we are attempting to debug this script
if __name__ == "__main__":
    pprint(scrape())
