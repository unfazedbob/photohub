import pymysql
from pymysql.constants import CLIENT

# 连接数据库的函数
def connection():
    conn = pymysql.connect(
        host='192.168.2.8',  # 数据库主机地址
        user='piggy',  # 数据库用户名
        password='123456',  # 数据库密码
        database='photohub',  # 数据库名称
        client_flag=CLIENT.MULTI_STATEMENTS,  # 允许执行多条SQL语句
        autocommit=True,  # 自动提交事务
    )
    return conn
