# 定义全局数据
from subs.usemysql import UseMysql

config = {
    'user': 'root',
    'password': '1qQO7DAfzz2kbj6L',
    'host': '36.138.74.151',
    'database': 'medical_records_core',
    'raise_on_warnings': True
}
use_sql = UseMysql()