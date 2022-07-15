# KARRIERE.AT SCRAPING
# This Python script uses Selenium which accesses the Firefox browser
# It opens the Austrian job ad platform "karriere.at",
# searches for all the terms in the list "search_list" and
# saves all the found jobs in "out.csv" with "," as separator and following columns:
# city, company_name, crawl_timestamp, job_description, job_title, job_type, post_date

# WHY IS THIS CODE NOT PART OF OUR JUPYTER NOTEBOOK?
# Unfortunately, we didn't manage to set the path the necessary driver (geckodriver.exe) in the jupyter environment.

# HOW TO INSTALL SELENIUM AND THE GECKODRIVER?
# Install Selenium with 'python -m pip install selenium'. See more: https://www.geeksforgeeks.org/how-to-install-selenium-in-python/
# Download driver from: https://github.com/mozilla/geckodriver/releases
# Unzip 'geckodriver-vxxxx.zip
# Set the path to driver on Windows: https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/amp/
# We had to restart system before it worked. Afterwards the code should run.

# WHERE DID WE LEARN HOW TO USE SELENIUM?
# We watched two very comprehensive YouTube tutorials from freeCodeCamp.org:
# - Web Scraping with Python - Beautiful Soup Crash Course. Link: https://www.youtube.com/watch?v=XVv6mJpFOb0
# - Selenium Course for Beginners - Web Scraping Bots, Browser Automation, Testing (Tutorial). Link: https://www.youtube.com/watch?v=j7VZsCCnptM

# CREDITS AND COPYRIGHT
# The code below was written by TeamBanov (Banov Aleksandar, Humer Matthias, Kapui Henriett)

import os
import sys
import pip
import time
import csv

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
# print(dir(driver))
driver.get("https://www.karriere.at/jobs")
driver.implicitly_wait(30)  # waiting up to _ seconds

# finding search form:
skill = driver.find_element(By.ID, "keywords")  # form "Was willst du machen?"
location = driver.find_element(By.ID, "locations")
# we won't use the "location" in our project, because we want to find offers from everywhere
submit = driver.find_element(By.CLASS_NAME, "m-jobsSearchform__submit")  # search button "Jobs finden"

### COOKIE POP-UP
# it appears not when opening the page but after some user action on the page (e.g. hovering mouse)
skill.send_keys(" ")  # activating cookie message
try:
    cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")  # accept cookies
    # cookies = driver.find_element(By.ID, "onetrust-reject-all-handler")  # reject cookies
    cookies.click()
    print("closed cookie pop-up")
    skill.clear()  # deleting input in skill
except:
    print("Skipping...")  # skipping if message doesn't appear... e.g. in case cookies are already accepted
    skill.clear()  # deleting input in skill

### LIST WITH ALL TERMS FOR SEARCH:
search_list = ["data science", "data engineer", "data scientist", "data analyst", "machine learning"]

### FOR LOOP FOR EARCH SEARCH TERM:
jobs = []  # this list will be expanded with all the job posts
for x in search_list:
    tmp = [] # a list which will be filled with results of each search term separately

    # because of some errors we need to find these two elements again:
    skill = driver.find_element(By.ID, "keywords")
    submit = driver.find_element(By.CLASS_NAME, "m-jobsSearchform__submit")

    skill.clear()  # deleting input in skill
    skill.send_keys(x)  # input x from search_list
    time.sleep(1)
    submit.click()  # click on "Jobs finden"


    ### JOB ALERT POP-UP
    # Now an annoying job alert pop-up might appear. (Usually only for the 1st round)
    # We try to close it:
    time.sleep(5)
    i = 10
    while (i > 0):
        i -= 1
        try:
            job_alert_close = driver.find_element(By.CLASS_NAME, "m-alarmDisruptor__closeSvg")
            job_alert_close.click()
            print("closed job alert pop-up")
            break
        except:
            print("didn't close job alert pop-up")
            time.sleep(1)

    # click on "show more jobs" - show all jobs :)
    # with a for loop we click on the "show more" button until end is reached
    click_more = True
    i = 1000  # for the abort condition; after i pages max it stops
    while click_more and (i > 0):
        try:
            time.sleep(2)
            load_more = driver.find_element(By.CLASS_NAME, "m-loadMoreJobsButton")
            load_more.click()
            print("clicking")
            i -= 1
        except:
            print("reached end or i reached limit")
            click_more = False

    # this list is the content of the left bar with all found jobs
    list = driver.find_elements(By.CLASS_NAME, "m-jobsListItem__titleLink")
    nr_jobs = len(list)  # number of job posts in the list

    for i in range(nr_jobs):
        # print(i)
        # time.sleep(1)
        list[i].location_once_scrolled_into_view  # this scrolls to the element - otherwise we cannot click on it
        list[i].click()  # clicking on job post
        time.sleep(1)

        # extracting info from job post:
        city = driver.find_element(By.CLASS_NAME, "m-jobHeader__jobLocations").text
        company_name = driver.find_element(By.CLASS_NAME, "m-jobHeader__companyLink").text
        crawl_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # inferred_salary_from
        # inferred_salary_time_unit
        # inferred_salary_to
        # inferred_state
        # is_remote
        job_title = driver.find_element(By.CLASS_NAME, "m-jobHeader__jobTitle").text
        job_type = driver.find_element(By.CLASS_NAME, "m-jobHeader__jobEmploymentTypes").text
        post_date = driver.find_element(By.CLASS_NAME, "m-jobHeader__jobDate").text
        # salary_offered
        # state

        # For the description we switch into an iframe:
        # for some job ads there is no info available
        # therefore try and except: in case there is no info, then it writes "null"
        try:
            iframe = driver.find_element(By.CLASS_NAME, "m-jobContent__iFrame--job")
            driver.switch_to.frame(iframe)
            job_description = driver.find_element(By.XPATH, "/html/body").text
            for j in range(5):  # removing double "\n"s and replacing \n with ;
                try:
                    job_description = job_description.replace('\n\n', '\n')
                except:
                    break
            job_description = job_description.replace('\n', ';')
            try:
                job_description = job_description.replace('"', '')
            except:
                pass
            # after scraping the job description in the iframe, we switch back to main page
            driver.switch_to.default_content()
        except:
            job_description = "null"

        ### SAVING INFO TO LIST
        # adding all information into a list
        job = []
        job.append(city)
        job.append(company_name)
        job.append(crawl_timestamp)
        job.append(job_description)
        job.append(job_title)
        job.append(job_type)
        job.append(post_date)

        # adding the list "job" to the final list "jobs"
        tmp.append(job)
        jobs.append(job)

    # this chunk is optional and not important
    # this creates just a temporary csv, in case an error occurs before finishing
    with open(x + "_tmp.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(tmp)
    print(x + " finished and exported")

### SAVING DATA TO CSV
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(jobs)

### DONE :D
print("Everything completed successfully")
# but:
#  +---+
#  |   |
#  O   |
# /|\  |
#      |
#      |
# almost dead
