from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import pause
import smtplib

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

load_dotenv()

config = open('config.json')
conf = json.load(config)

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

USERNAME = os.environ.get("TOCK_USERNAME")
PASSWORD = os.environ.get("TOCK_PASSWORD")
RELEASE_YEAR = conf['release-year']
RELEASE_MONTH = conf['release-month']
RELEASE_DAY = conf['release-day']
RELEASE_TIME_24_HOUR_UTC = conf['release-time-24-utc']
EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
CARRIER = os.environ.get("CARRIER")

RESTAURANT = conf['restaurant-code']
PARTY_SIZE = conf['party-size']

DATES = conf['dates']


def send_message(msg):
    recipient = PHONE_NUMBER + CARRIERS[CARRIER]
    auth = (EMAIL_USERNAME, EMAIL_PASSWORD)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, msg)

driver = webdriver.Chrome()
driver.get("https://www.exploretock.com/login?continue=%2F")

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "email")))
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "password")))
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='signin']")))
driver.find_element(By.ID, "email").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[@data-testid='signin']").click()

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='search-button']")))

driver.get(f"https://www.exploretock.com/{RESTAURANT}")

print("On restaurant home page, now waiting for release time...")
dt = datetime(int(RELEASE_YEAR), int(RELEASE_MONTH), int(RELEASE_DAY), int(RELEASE_TIME_24_HOUR_UTC))
pause.until(dt)
print("GOT TO TIME")

def find_option():
    for date in DATES:
        driver.get(f"https://www.exploretock.com/{RESTAURANT}/search?date={date}&size={PARTY_SIZE}&time=12%3A00")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='SearchModal-body']")))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='SearchBarModalContainer']")))
        # time.sleep(4)
        options = driver.find_elements(By.XPATH, "//button[contains(@class, 'is-available') and contains(@class, 'Consumer-resultsListItem')]")
        options.reverse()
        for option in options:
            option.click()
            send_message("A spot have been found!")
            return
    send_message("Spot not found...")
find_option()
time.sleep(1000)
driver.quit()