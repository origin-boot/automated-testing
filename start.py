import unittest
from BeautifulReport import BeautifulReport
from testcase.LoginTest import TestLoginAdmin
from testcase.SystemManage import TestSystemManage

if __name__=='__main__':

        suite = unittest.TestSuite() #定义一个测试套件

        suite.addTests(unittest.makeSuite(TestLoginAdmin)) #这个类里面所有的测试用例
        suite.addTests(unittest.makeSuite(TestSystemManage))

#       suite.addTest(TestCalc(‘test_pass_case‘)) #单个添加用例

        result = BeautifulReport(suite)      #使用BeautifulReport产出测试报告
        result.report(filename="住院病案首页测试报告", description="测试结果") # 默认在当前路径下，可以加log_path