import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginAdmin:
    def __init__(self, driver):
        self.driver = driver
        self.login_url = "http://demo.smr.shuzhiqiyuan.com/#/login"

    def open_login_page(self):
        self.driver.get(self.login_url)
        self.driver.maximize_window()
        time.sleep(2)

    def login(self, username, password):
        self.open_login_page()
        element_users = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='账号']"))
        )
        element_users.send_keys(username)
        element_password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='密码']"))
        )
        element_password.send_keys(password)
        self.driver.find_element(By.TAG_NAME, "button").click()


