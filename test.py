#from bs4 import BeautifulSoup as BS
#import requests
from selenium import webdriver
import time
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys

pages_array = []
jobs_array = []
theJob = "software+engineer"
home_page = "https://www.indeed.com/jobs?q=" + theJob + "&l="


def get_web_driver(the_url):
    browser = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
    browser.set_page_load_timeout("5")
    browser.get(the_url)
    return browser


def close_web_driver(browser):
    time.sleep(5)
    browser.quit()


def page_parse(the_url):

    # browser.find_element_by_id("sja1").click()
    browser = get_web_driver(the_url)
    jobs = browser.find_elements_by_xpath("//*[contains(@class,'row result clickcard')]") # go through each box

    for items in jobs:
        job = items.find_element_by_class_name('snip') # tip: class="sjCapt" class = "iaP"
        description = job.text
        if description.find("Easily apply") != -1:
            job_title = items.find_element_by_tag_name("a").text
            company = items.find_element_by_class_name("company").text
            location = items.find_element_by_class_name("location").text
            #print(job_title + "\n" + company + "\n" + location)
            a = items.find_element_by_xpath(".//a")
            url = a.get_attribute("href")
            jobs_array.append(url)
            print(url)


page_parse(home_page)
