from testcase.__globe import config
import mysql.connector


class UseMysql:
    def useMysql(self, query, params=None):
        try:
            # 使用with语句自动管理连接和游标的关闭
            with mysql.connector.connect(**config) as conn:
                with conn.cursor() as cursor:
                    # 执行参数化查询
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    # 获取所有查询结果
                    return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"数据库操作出现错误: {e}")
            # 可选：根据需求决定是否要抛出异常或返回错误代码
            raise
        except Exception as e:
            print(f"非数据库相关错误: {e}")
            raise
