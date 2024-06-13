# -*- coding: utf-8 -*-
import re
import time
import unittest

import mysql.connector
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from web.login import LoginAdmin


class TestUserManage(unittest.TestCase):

    # 定义全局数据
    config = {
        'user': 'root',
        'password': '1qQO7DAfzz2kbj6L',
        'host': '36.138.74.151',
        'database': 'medical_records_core',
        'raise_on_warnings': True
    }
    Hospital_Code = "SZQY_MEDICAL"
    Hospital_Name = "数智起源-Medical"
    Medical_code = "641300"
    Manager_name = "数智起源"
    Insert_name = "数智起源"
    Insert_phone = "0000-14332232"
    Statistics_name = "数智起源"
    Statistics_phone = "0000-14332233"
    test_failed = False
    user_status = '0'
    def setUp(self):

        # 初始化页面
        self.driver = webdriver.Chrome()
        self.login_admin = LoginAdmin(self.driver)
        self.login_admin.login("admin", "admin123")

        # 找到系统管理菜单并进行点击
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='系统管理']"))
        )
        element.click()

        # 找到用户管理菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='用户管理']"))
        )
        element.click()


    # 新增用户
    def  test_countUsers(self):

        # 查询用户页面所有数据对比数据库，是否一致
        # 获取页面用户数量总计
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "is-first"))
        )
        elements = element.text
        usernums = re.findall(r'\d+', elements)
        if usernums:
            usernum = int(usernums[0])


        # 查询数据库用户总计，并进行对比
        conn = mysql.connector.connect(**self.config)
        self.assertTrue(conn.is_connected(), "数据库连接失败")

        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT count(*) as num FROM sys_user WHERE del_flag = 0 ;")  # 执行查询
        num = cursor.fetchone()[0]  # 获取查询结果
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

        # 断言数据库中的用户数和页面上显示的用户数是否一致
        self.assertEqual(num, usernum, f"用户查询有误，页面显示: {usernum}条, 数据库: {num}条")

    def test_searchUsers(self):

        # 查询数据库用户总计，并进行对比
        conn = mysql.connector.connect(**self.config)
        self.assertTrue(conn.is_connected(), "数据库连接失败")

        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT user_name, nick_name  FROM sys_user WHERE del_flag = 0 limit 5;")  # 执行查询
        usernames = cursor.fetchall()  # 获取查询结果
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

        # 循环遍历查询账号，并传入查询框中进行查询，对比结果
        for username in usernames:
            user = username[0]
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入用户账号']"))
            )
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(1)
            element.send_keys(user)
            time.sleep(1)
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[3]/div"))
            )
            account = element.text
            # 断言数据库中的用户数和页面上显示的用户数是否一致
            try :
                self.assertEqual(user, account, f"用户查询有误，查询条件: {user}, 查询结果: {account}")
            except AssertionError as e:
                print(e)
                self.test_failed = True

            time.sleep(1)

        # 清空前置查询
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入用户账号']"))
        )
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACK_SPACE)

        for username in usernames:
            nick = username[1]
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入用户昵称']"))
            )
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACK_SPACE)
            time.sleep(1)
            element.send_keys(nick)
            time.sleep(1)
            try:
                # 尝试找到元素，等待最多10秒
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      "/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[4]/div"))
                )
                # 如果找到了元素，执行一些操作
                print("找到元素：", element.text)
            except TimeoutException:
                # 如果找不到元素，打印提示信息但不停止程序
                print("未查询到数据")
                self.test_failed = True
            name = element.text
            # 断言数据库中的用户数和页面上显示的用户数是否一致
            try :
                self.assertEqual(nick, name, f"用户查询有误，查询条件: {nick}, 查询结果: {name}")
            except AssertionError as e:
                print(e)
                self.test_failed = True
            time.sleep(3)
        if self.test_failed == True:
            self.fail("用例失败")
    def test_searchCountStatus(self):

        # 查询用户页面所有数据对比数据库，是否一致
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='用户状态']"))
        )
        element.click()
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-select-dropdown__item"))
        )
        for element in elements:
            if "正常" in element.text:
                element.click()
                break
        time.sleep(2)
        # 获取页面用户数量总计
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "is-first"))
        )
        elements = element.text
        usernums = re.findall(r'\d+', elements)
        if usernums:
            usernum = int(usernums[0])

        # 查询数据库用户总计，并进行对比
        conn = mysql.connector.connect(**self.config)
        self.assertTrue(conn.is_connected(), "数据库连接失败")

        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT count(*) as num FROM sys_user WHERE del_flag = 0 and status = 0;")  # 执行查询
        num = cursor.fetchone()[0]  # 获取查询结果
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

        # 断言数据库中的用户数和页面上显示的用户数是否一致
        self.assertEqual(num, usernum, f"用户查询有误，页面显示: {usernum}条, 数据库: {num}条")

    # def test_searchCountDate(self):
    #
    #
    def tearDown(self):
        self.driver.quit()
