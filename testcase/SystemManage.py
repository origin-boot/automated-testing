import time
import unittest

import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from web.login import LoginAdmin


class TestSystemManage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_admin = LoginAdmin(self.driver)

    def test_Hospital_Maintenance(self):

        # 页面输入框值定义
        Hospital_Code = "SZQY_MEDICAL"
        Hospital_Name = "数智起源-Medical"
        Medical_code = "641300"
        Manager_name = "数智起源"
        Insert_name = "数智起源"
        Insert_phone = "0000-14332232"
        Statistics_name = "数智起源"
        Statistics_phone = "0000-14332233"

        # 登录到系统
        self.login_admin.login("admin", "admin123")


        # 找到系统管理菜单并进行点击
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='系统管理']"))
        )
        element.click()


        # 找到医院信息维护菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='医院信息维护']"))
        )
        element.click()


        time.sleep(2)  # 等待页面元素加载


        # 插入医院机构代码
        # 对页面元素进行输入新值并保存
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[1]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Hospital_Code)


        # 插入医院机构名称
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[2]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Hospital_Name)


        # 插入医院机构地区编码
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[3]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Medical_code)



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
        element.send_keys(Manager_name)


        # 插入录入负责人
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[2]/div[3]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Insert_name)

        # 插入录入负责人电话
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div[1]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Insert_phone)

        # 插入统计负责人
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div[2]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Statistics_name)

        # 插入统计负责人电话
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div[3]/div/div/div/div/input"))
        )
        element.clear()
        element.send_keys(Statistics_phone)


        # 点击保存按钮
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[4]/div/button"))
        )
        element.click()


        # 进行数据库查询,并进行对比，查看数据是否保存成功
        config = {
            'user': 'root',
            'password': '1qQO7DAfzz2kbj6L',
            'host': '36.138.74.151',
            'database': 'medical_records_core',
            'raise_on_warnings': True
        }

        conn = mysql.connector.connect(**config)

        # 检查是否连接成功
        if conn.is_connected():
            print('成功连接到数据库')
        cursor = conn.cursor()  # 创建游标对象

        query = "SELECT code, name,  area_code, medical_type, unit_personnel, fill_personnel, fill_landline, count_personnel,count_phone FROM  hospital_config;"  # 编写 SQL 查询
        cursor.execute(query)  # 执行查询
        row = cursor.fetchone()
        cursor.close()  # 关闭游标
        if row:
            code, name, area_code, medical_type, unit_personnel, fill_personnel, fill_landline, count_personnel, count_phone = row
            if code == Hospital_Code and name == Hospital_Name and area_code == Medical_code and medical_type == '4' and unit_personnel == Manager_name and fill_personnel == Insert_name and fill_landline == Insert_phone and count_personnel == count_personnel and count_phone == count_phone:
                print('医疗机构信息数据保存无误')
                return None
            else:
                print('医疗机构信息数据保存有误')
                return False


    def tearDown(self):
        self.driver.quit()
