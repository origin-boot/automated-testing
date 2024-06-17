# -*- coding: utf-8 -*-
import random
import re
import string
import time
import unittest

import mysql.connector
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from subs.login import LoginAdmin
from __globe import config
from subs.usemysql import UseMysql
from subs.IdNumber import generate_id_number



class TestUserManage(unittest.TestCase):
    test_failed = False
    user_status = '0'
    use_sql = UseMysql()
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
    def test_countUsers(self):

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
        query = "SELECT count(*) as num FROM sys_user WHERE del_flag = 0 ;"  # 执行查询
        nums = self.use_sql.useMysql(query)
        num = nums[0][0]
        # 断言数据库中的用户数和页面上显示的用户数是否一致
        self.assertEqual(num, usernum, f"用户查询有误，页面显示: {usernum}条, 数据库: {num}条")

    def test_searchUsers(self):

        # 查询数据库用户总计，并进行对比
        query = "SELECT user_name, nick_name  FROM sys_user WHERE del_flag = 0 limit 5;" # 执行查询
        usernames = self.use_sql.useMysql(query)

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
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[3]/div"))
            )
            account = element.text
            # 断言数据库中的用户数和页面上显示的用户数是否一致
            try:
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
            try:
                self.assertEqual(nick, name, f"用户查询有误，查询条件: {nick}, 查询结果: {name}")
            except AssertionError as e:
                print(e)
                self.test_failed = True
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
        conn = mysql.connector.connect(**config)
        self.assertTrue(conn.is_connected(), "数据库连接失败")

        cursor = conn.cursor()  # 创建游标对象
        query = "SELECT count(*) as num FROM sys_user WHERE del_flag = 0 and status = 0;"  # 执行查询
        num = self.use_sql.useMysql(query)  # 获取查询结果
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接

        # 断言数据库中的用户数和页面上显示的用户数是否一致
        self.assertEqual(num, usernum, f"用户查询有误，页面显示: {usernum}条, 数据库: {num}条")

    def test_searchCountDate(self):

        # 日期开始及日期结束进行传参
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='开始日期']"))
        )
        element.send_keys("2023-11-01")

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='结束日期']"))
        )
        element.send_keys("2023-11-30")
        element.send_keys(Keys.ENTER)

        # 查询等待时间，保证数据加载正确
        time.sleep(1)

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
        query = "SELECT count(*) as num FROM sys_user WHERE del_flag = 0 and create_time >= '2023-11-01 00:00:00' and create_time <= '2023-11-30 23:59:59' ;" # 执行查询
        nums = self.use_sql.useMysql(query)  # 获取查询结果
        num = nums[0][0]
        # 断言数据库中的用户数和页面上显示的用户数是否一致
        self.assertEqual(num, usernum, f"用户查询有误，页面显示: {usernum}条, 数据库: {num}条")

    def tearDown(self):
        self.driver.quit()


class TestInsertUser(unittest.TestCase):
    use_sql = UseMysql()
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

    def test_insert_user(self):

        # 进入新增页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/div/div[2]/div[1]/div[1]/button"))
        )
        element.click()
        time.sleep(2)
        # 获取一个随机5位字母的字符串 用于昵称及账号
        name = ''.join(random.choices(string.ascii_letters, k=8))
        # 用户昵称
        elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[placeholder='请输入用户昵称']"))
        )
        element = elements[1]
        element.send_keys(name)

        # 用户账号
        elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[placeholder='请输入用户账号']"))
        )
        element = elements[1]
        element.send_keys(name)

        # 用户密码
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='请输入用户密码']"))
        )
        element.send_keys("123456")

        # 用户角色
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[4]/div/div/div/form/div[1]/div[2]/div/div/div/div/div[1]/div[2]"))
        )
        element.click()

        # 定位角色的下拉框，并随机选择进行点击
        # 获取所有下拉项
        element_roles = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-select-dropdown__item"))
        )

        # 查询数据库角色，通过获取比对进行勾选
        query = "SELECT role_name  FROM sys_role where del_flag = 0 and role_key !='admin';"  # 执行查询
        roles = self.use_sql.useMysql(query)# 获取查询结果
        # 随机选择第一个元素并点击
        first_index = random.randint(0, len(roles) - 1)
        role = roles[first_index]
        for element_role in element_roles:
            if str(role[0]) == str(element_role.text):
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_role)
                element_role.click()
                break
        # element = WebDriverWait(self.driver, 15).until(
        #     EC.visibility_of_element_located(
        #         (By.XPATH, "/html/body/div[4]/div/div/div/form/div[1]/div[2]/div/div/div/div/div[1]/div[2]"))
        # )
        # element.click()


        # 用户性别
        element_select = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "el-select__placeholder"))
        )
        element_select[3].click()

        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-select-dropdown__item"))
        )
        # 随机选择第一个元素并点击
        # 查询数据库角色，通过获取比对进行勾选
        query = "SELECT dict_label FROM sys_dict_data where dict_type = 'sys_user_sex';"  # 执行查询
        sexs_sql = UseMysql()
        sexs = sexs_sql.useMysql(query)# 获取查询结果

        # 随机选择第一个元素并点击
        sex_index = random.randint(0, len(sexs) - 1)
        sex = sexs[sex_index]
        for element in elements:
            if sex[0] == element.text:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                break

        # 科室选择
        element_select = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "el-select__placeholder"))
        )
        element_select[4].click()

        # 定位科室的下拉框，并随机选择多选两个下拉框进行点击
        # 获取所有下拉项
        element_depts = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-select-dropdown__item"))
        )

        # 查询数据库科室，通过获取比对进行勾选
        query = "SELECT dept_name  FROM sys_dept where del_flag = 0 and status = 0;" # 执行查询
        depts = self.use_sql.useMysql(query)# 获取查询结果
        # 随机选择第一个元素并点击
        first_index = random.randint(0, len(depts) - 1)
        first_dept = depts[first_index]
        for element_dept in element_depts:
            if str(first_dept[0]) == str(element_dept.text):
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_dept)
                element_dept.click()
                break
        # 随机选择第二个元素并点击
        depts.pop(first_index)  # 删除已选择好的数据
        second_index = random.randint(0, len(depts) - 1)
        second_dept = depts[second_index]
        for element_dept2 in element_depts:
            if str(second_dept [0]) == str(element_dept2.text):
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_dept2)
                element_dept2.click()
                break

        # 身份证
        element_insert = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='身份号']"))
            )
        element_insert.send_keys(generate_id_number())

        #
        query = "select role_key from sys_role where role_name = %s "
        role_keys = self.use_sql.useMysql(query,role)
        if str(role_keys[0][0]) == "doctor" or str(role_keys[0][0]) != "doctor":
           # a = random.choice([1, 2])
            a = 2
            if a == 1:
                # element_on = WebDriverWait(self.driver, 15).until(
                #     EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/form/div[6]/div/div/div/div/span/div"))
                # )
                # element_on.click()
                self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div/form/div[6]/div/div/div/div/span/div").click()
                # 添加医生证书编码
                doctor_code = ''.join(random.choices(string.digits, k=8))
                element_doctor = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/form/div[7]/div[1]/div/div/div/div/input"))
                )
                element_doctor.send_keys(doctor_code)
                element_doctor = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/form/div[7]/div[2]/div/div/div/div/input"))
                )
                element_doctor.send_keys(doctor_code)
                element_doctor = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/form/div[8]/div/div/div/div/div/input"))
                )
                element_doctor.send_keys(doctor_code)
            else:
                # element_on = WebDriverWait(self.driver, 15).until(
                #     EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/form/div[7]/div/div/div/div/input"))
                # )
                # element_on.click()
                self.driver.find_element(By.XPATH,"/html/body/div[5]/div/div/div/form/div[10]/div/div/div/div/span").click()

                # 添加护士证书编码
                nurse_code = ''.join(random.choices(string.digits, k=8))
                element_nurse = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='护士职业证书编号']"))
                )
                element_nurse.send_keys(nurse_code)
                element_nurse = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/form/div[12]/div/div/div/div/div/input"))
                )
                element_nurse.send_keys(nurse_code)

        # 备注
        element_remark = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "el-textarea__inner"))
        )
        element_remark.send_keys("自动化测试数据生成")

        # 点击保存
        # element_save = WebDriverWait(self.driver, 15).until(
        #     EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/footer/div/button[2]/span"))
        # )
        self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/footer/div/button[2]/span").click()
        # print(element_save.text)
        # time.sleep(2)
        # element_save.click()
        self.driver.save_screenshot("userinsert_result_screenshot.png")

        query = "select user_name from sys_user where user_name = %s "
        result = self.use_sql.useMysql(query, name)
        self.assertEqual(result[0][0], name, f"用户新增有误，数据库查询账号: {result[0][0]}, 新增输入账号: {name}")
        print(result[0][0])
        print(name)




