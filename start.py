import unittest
from BeautifulReport import BeautifulReport
from testcase.LoginTest import TestLoginAdmin
from testcase.UserManage import TestUserManage
from testcase.HospitalInfomation import T

if __name__ == '__main__':
    # 定义一个测试套件
    suite = unittest.TestSuite()

    # 使用 TestLoader 来加载测试用例
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestLoginAdmin))  # 这个类里面所有的测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestUserManage))
    suite.addTests(loader.loadTestsFromTestCase(TestLoginAdmin))

    # 使用 BeautifulReport 生成测试报告
    result = BeautifulReport(suite)
    result.report(filename="住院病案首页测试报告", description="测试结果")  # 默认在当前路径下，可以加log_path