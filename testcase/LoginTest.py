# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from web.login import LoginAdmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestLoginAdmin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_admin = LoginAdmin(self.driver)

    def test_login_success(self):
        self.login_admin.login("admin", "admin123")
        # 添加断言来验证登录是否成功
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sidebar-title"))
        )
        self.assertIsNotNone(element)

    def test_login_failure(self):
        self.login_admin.login("admin", "wrongpassword")
        # 添加断言来验证登录失败
        message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title"))  # 使用合适的选择器
        )
        message_text = message_element.text
        print("Captured Message:", message_text)
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
