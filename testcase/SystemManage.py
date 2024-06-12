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


class TestSystemManage(unittest.TestCase):

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

    def test_Hospital_Maintenance(self):

        # 找到医院信息维护菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='医院信息维护']"))
        )
        element.click()


        # 插入医院机构代码
        # 对页面元素进行输入新值并保存
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[1]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Hospital_Code)


        # 插入医院机构名称
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[2]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Hospital_Name)


        # 插入医院机构地区编码
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[3]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Medical_code)



        # 插入医疗机构类型
        # 找到下拉框
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[2]/div[1]/div/div/div/div/div/div/input"))
        )
        # 点击下拉框以激活它
        element.click()
        # 如果输入后下拉选项自动出现，等待并选择下拉选项
        # 循环遍历下拉框数据 找到4：西医时进行点击操作
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-select-dropdown__item"))
        )
        for element in elements:
            if "4:西医" in element.text:
                element.click()
                break


        # 插入医院机构负责人
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[2]/div[2]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Manager_name)


        # 插入录入负责人
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[2]/div[3]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Insert_name)

        # 插入录入负责人电话
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div[1]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Insert_phone)

        # 插入统计负责人
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div[2]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Statistics_name)

        # 插入统计负责人电话
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div[3]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(self.Statistics_phone)


        # 点击保存按钮
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[4]/div/button"))
        )
        element.click()


        # 进行数据库查询,并进行对比，查看数据是否保存成功
        conn = mysql.connector.connect(**self.config)

        # 检查是否连接成功
        if conn.is_connected():
            print('成功连接到数据库')
        cursor = conn.cursor()  # 创建游标对象

        query = "SELECT code, name,  area_code, medical_type, unit_personnel, fill_personnel, fill_landline, count_personnel,count_phone FROM  hospital_config;"  # 编写 SQL 查询
        cursor.execute(query)  # 执行查询
        row = cursor.fetchone()
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        if row:
            code, name, area_code, medical_type, unit_personnel, fill_personnel, fill_landline, count_personnel, count_phone = row
        self.assertEqual(code, self.Hospital_Code, "医院代码不正确")
        self.assertEqual(name, self.Hospital_Name, "医院名称不正确")
        self.assertEqual(area_code, self.Medical_code, "机构地区编码不正确")
        self.assertEqual(medical_type, "4", "医疗机构类型不正确")
        self.assertEqual(unit_personnel, self.Manager_name, "机构负责人不正确")
        self.assertEqual(fill_personnel, self.Insert_name, "录入负责人不正确")
        self.assertEqual(fill_landline, self.Insert_phone, "录入负责人电话不正确")
        self.assertEqual(count_personnel, self.Statistics_name, "统计负责人不正确")
        self.assertEqual(count_phone, self.Statistics_phone, "统计负责人电话不正确")

    # 新增用户
    def  test_countUsers(self):

        # 找到用户管理菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='用户管理']"))
        )
        element.click()

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
        # 找到用户管理菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='用户管理']"))
        )
        element.click()

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
    def test_searchCountUsers(self):
        # 找到用户管理菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='用户管理']"))
        )
        element.click()

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


    def tearDown(self):
        self.driver.quit()
