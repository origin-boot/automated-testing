# -*- coding: utf-8 -*-
import random
import time
import unittest

import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from New_medical.obj.login import LoginAdmin
from New_medical.__globe import config

class TestHospitalManage(unittest.TestCase):

    # 定义全局数据
    Hospital_Code = "SZQY_MEDICAL"
    Hospital_Name = "数智起源-Medical"
    Medical_code = "641300"
    Manager_name = "数智起源"
    Insert_name = "数智起源"
    Insert_phone = "0000-14332232"
    Statistics_name = "数智起源"
    Statistics_phone = "0000-14332233"
    test_failed = False

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

        # 找到医院信息维护菜单进行点击跳转到页面
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='医院信息维护']"))
        )
        element.click()
        time.sleep(1)
        self.driver.refresh()
    def test_Hospital_Maintenance(self):


        # 插入医院机构代码
        # 对页面元素进行输入新值并保存
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable
                ((By.XPATH, "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div[1]/div/div/div/div/input"))
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
                (By.CLASS_NAME, "m-2"))
        )
        # 点击下拉框以激活它
        element.click()
        # 如果输入后下拉选项自动出现，等待并选择下拉选项
        # 循环遍历下拉框数据 随机进行点击操作
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-select-dropdown__item"))
        )
        first_index = random.randint(0, len(elements) - 1)
        element = elements[first_index]
        time.sleep(1)
        element.click()
        if element.text == "1:中医":
            Hospital_type = "1"
        elif element.text == "2:民族医":
            Hospital_type = "2"
        elif element.text == "3:中西医":
            Hospital_type = "3"
        else:
            Hospital_type = "4"
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
                (By.CLASS_NAME, "el-button--primary"))
        )
        element.click()

        time.sleep(3)
        # 进行数据库查询,并进行对比，查看数据是否保存成功
        conn = mysql.connector.connect(**config)

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
        self.assertEqual(medical_type, Hospital_type, "医疗机构类型不正确")
        self.assertEqual(unit_personnel, self.Manager_name, "机构负责人不正确")
        self.assertEqual(fill_personnel, self.Insert_name, "录入负责人不正确")
        self.assertEqual(fill_landline, self.Insert_phone, "录入负责人电话不正确")
        self.assertEqual(count_personnel, self.Statistics_name, "统计负责人不正确")
        self.assertEqual(count_phone, self.Statistics_phone, "统计负责人电话不正确")
