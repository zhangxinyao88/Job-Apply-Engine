from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
def get_web_driver(the_url):
    browser = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
    browser.set_page_load_timeout("5")
    browser.get(the_url)
    return browser
'''


def answer_info(driver):
    while not driver.find_element_by_xpath("//*[@id='form-action-submit']"):
        questions = driver.find_elements_by_class_name("input")
        for question in questions: # answer the questions
            question.click()
        # continue to next page
        driver.find_element_by_xpath("//*[@id='form-action-continue']").click()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath('//iframe')))
        i_frame = driver.find_element_by_tag_name("iframe")
        driver.switch_to.frame(i_frame)
    driver.find_element_by_xpath("//*[@id='form-action-submit']").click()


user_first_name = "Xinyao"
user_last_name = "Zhang"
user_Email = "zhangxinyao88@gmail.com"
resume_rep = "D:\Resume:\Sample.txt"


job_page = "https://www.indeed.com/viewjob?jk=1715bbb95511d8be&from=serp&vjs=3"
driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
driver.set_page_load_timeout("5")
driver.get(job_page)

driver.find_element_by_xpath("//*[@id='indeedApplyButtonContainer']").click()  # find and click the apply button
#  question = browser.find_element_by_xpath("//*[@id='label-input-applicant.firstName']")
#  question = browser.find_element_by_id("label-input-applicant.fistName")
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath('//iframe')))
# presence_of_element_located((By.XPATH, "/html/body/iframe")))
# popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "indeed-apply-popup")))
i_frame = driver.find_element_by_tag_name("iframe")
    # find_elements_by_xpath('//iframe')
driver.switch_to.frame(i_frame) # switch to the pop up window with name ( or first name, last name), email and resume
# name_field = driver.find_element_by_class_name("UserField-Name")
# names = name_field.find_elements_by_class_name("ia-TextInput")
# for name in names:

# check if the question is first name and last name or full name

first_name = driver.find_element_by_xpath("//*[@id='label-input-applicant.firstName']/label")
if first_name:                                                                           # first + last name
    first_name_space = driver.find_element_by_xpath("//*[@id='input-applicant.firstName']")
    first_name_space.send_keys(user_first_name)

last_name = driver.find_element_by_xpath("//*[@id='label-input-applicant.lastName']/label")
if last_name:
    last_name_space = driver.find_element_by_xpath("//*[@id='input-applicant.lastName']")
    last_name_space.send_keys(user_last_name)
else:
    name_space = driver.find_element_by_xpath("//*[@id='label-input-applicant.name']/label")  # full name
    name_space.send_keys(user_first_name + " " + user_last_name)

# Email
Email_space = driver.find_element_by_xpath("//*[@id='input-applicant.email']")
Email_space.send_keys(user_Email)

# Resume
resume_button = driver.find_element_by_xpath("//*[@id='ia-FilePicker-resume']")
resume_button.send_keys("C:/Users/zhang/Desktop/Sum.docx")

# Click continue button
driver.find_element_by_xpath("//*[@id='form-action-continue']").click()

WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name("iframe")))
i_frame2 = driver.find_element_by_tag_name("iframe")
driver.switch_to.frame(i_frame2)

questions = driver.find_elements_by_class_name("input")
for question in questions:  # answer the questions
    print(question.text)
    question.click()
driver.find_element_by_xpath("//*[@id='form-action-submit']").click()

# answer_info(driver)

