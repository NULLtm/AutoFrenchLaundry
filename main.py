from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from datetime import datetime
import pause
import smtplib

import time

load_dotenv()

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
RELEASE_YEAR = os.environ.get("RELEASE_YEAR")
RELEASE_MONTH = os.environ.get("RELEASE_MONTH")
RELEASE_DAY = os.environ.get("RELEASE_DAY")
RELEASE_TIME_24_HOUR_UTC = os.environ.get("RELEASE_TIME_24_HOUR_UTC")
EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
CARRIER = os.environ.get("CARRIER")

YEAR = os.environ.get("YEAR")
MONTH = os.environ.get("MONTH")
DAY = os.environ.get("DAY")
TIME = os.environ.get("TIME")
AM_PM = os.environ.get("AM_PM")


def send_message():
    recipient = PHONE_NUMBER + CARRIERS[CARRIER]
    auth = (EMAIL_USERNAME, EMAIL_PASSWORD)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, "Hi Mom, let me know if you recieve this automated message... please send your response to my normal number and not this bot! - Owen")

driver = webdriver.Chrome()
driver.get("https://www.exploretock.com/tfl/")
time.sleep(5)
driver.find_element(By.XPATH, "//span[text()='Log in']//..").click()
time.sleep(5)
driver.find_element(By.ID, "email").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[@data-testid='signin']").click()
time.sleep(5)
driver.find_element(By.XPATH, "//a[@data-testid='offering-book-button_DiningRoom']").click()

dt = datetime(int(RELEASE_YEAR), int(RELEASE_MONTH), int(RELEASE_DAY), int(RELEASE_TIME_24_HOUR_UTC))
pause.until(dt)
print("GOT TO TIME")
month = driver.find_element(By.XPATH, f"//span[text()='{MONTH + ' ' + YEAR}']//..//..//..")
month.find_element(By.XPATH, f"//span[text()={DAY}]//..").click()
time.sleep(3)
driver.find_element(By.XPATH, f"//div[@class='SearchModal-body']//span[text()={TIME + ' ' + AM_PM}]//..//..//..").click()
time.sleep(3)
#send_message("Found a spot")

driver.quit()