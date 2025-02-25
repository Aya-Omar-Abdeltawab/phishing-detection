import configparser
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

config = configparser.ConfigParser()
config.read('config.ini')

EMAIL = config['facebook']['email']
PASSWORD = config['facebook']['password']
CHROME_PATH = config['selenium']['chrome_path']
PIN = config['chat']['pin']
CONTACT = config['chat']['contact']
SCROLLS = int(config['chat']['scrolls'])

driver = webdriver.Chrome()
driver.get("https://www.facebook.com")
time.sleep(2)
email_input = driver.find_element(By.ID, "email")
email_input.send_keys(EMAIL)

password_input = driver.find_element(By.ID, "pass")
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)
time.sleep(5)
driver.get("https://www.facebook.com/messages/t/")
time.sleep(5)
pin_input = driver.find_element(By.ID, "mw-numeric-code-input-prevent-composer-focus-steal")
pin_input.send_keys(PIN)
time.sleep(10)
chat_div = driver.find_element(By.XPATH, f"//span[contains(text(), '{CONTACT}')]")
chat_div.click()
time.sleep(5)
chat_page = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Messages in conversation with')]")
messages = []
for _ in range(10):
    msg_blocks = chat_page.find_elements(By.XPATH, ".//div[@dir='auto']")
    for block in msg_blocks:
        try:
            if block.text not in messages:
                messages.append(block.text)
        except:
            print("No text msg")
    driver.execute_script("arguments[0].scrollTop = 0;", chat_page)
    time.sleep(2)

with open('messages.json', 'w', encoding='utf-8') as json_file:
    json.dump(messages, json_file, ensure_ascii=False, indent=4)
