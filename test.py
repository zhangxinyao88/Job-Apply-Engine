#from bs4 import BeautifulSoup as BS
#import requests
from selenium import webdriver
import time
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys

theJob = "software+engineer+intern"
url = "https://www.indeed.com/jobs?q=" + theJob + "&l="
browser = webdriver.Chrome('C:\chromedriver\chromedriver.exe')

browser.set_page_load_timeout("5")
browser.get(url)
#browser.find_element_by_id("sja1").click()

Jobs = browser.find_elements_by_xpath("//*[contains(@class,'row result clickcard')]")
for items in Jobs:
    job = items.find_element_by_xpath("//*[@class='snip']")
    print(job.text)
time.sleep(10)
#browser.quit()
