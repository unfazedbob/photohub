import pymysql
from pymysql.constants import CLIENT

def connection():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='photohub',
        client_flag=CLIENT.MULTI_STATEMENTS,
        autocommit=True,
    )
    return conn
