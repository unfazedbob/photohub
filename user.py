import hashlib

from flask import request, session
import pymysql

from db import connection

# 获取用户登录状态的API接口
# /api/user/status
def status():
    # 检查session中是否存在user_id，如果不存在则表示用户未登录
    if 'user_id' not in session:
        return {
            'logined': False
        }
    # 使用数据库连接进行查询
    with connection().cursor() as cur:
        sql = 'SELECT username FROM user WHERE id = %s'
        cur.execute(sql, (int(session['user_id'])))
        username = cur.fetchone()[0]
        return {
            'logined': True,
            'username': username,
        }
    
# 用于密码哈希的密钥
secret_key = 'photohubxstdgmhjxvsptbpzvgzxfnvqv'

# 用户注册的API接口
# /api/user/register
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    # 使用BLAKE2b算法对密码进行哈希处理
    password_hash = hashlib.blake2b((password + secret_key).encode()).hexdigest()

    with connection().cursor() as cur:
        sql = 'INSERT INTO user (username, password_hash) VALUES (%s, %s)'
        try:
            cur.execute(sql, (username, password_hash))
        except pymysql.err.IntegrityError:
            # 如果用户名已存在，清除session并返回错误信息
            session.clear()
            return {
                'logined': False,
                'message': '用户名已存在'
            }

        # 将新注册用户的ID保存到session中
        session['user_id'] = cur.lastrowid
        return {
            'logined': True,
            'username': username,
        }

# 用户登录的API接口
# /api/user/login
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # 使用BLAKE2b算法对密码进行哈希处理
    password_hash = hashlib.blake2b((password + secret_key).encode()).hexdigest()

    with connection().cursor() as cur:
        sql = 'SELECT id FROM user WHERE username = %s AND password_hash = %s'
        cur.execute(sql, (username, password_hash))
        data = cur.fetchone()
        if data is None:
            # 如果用户名或密码错误，返回错误信息
            return {
                'logined': False,
                'message': '用户名或密码错误'
            }
        
        # 将用户ID保存到session中
        session['user_id'] = data[0]
        return {
            'logined': True,
            'username': username,
        }

# 用户登出的API接口
# /api/user/logout
def logout():
    # 清除session
    session.clear()
    return {
        'logined': False,
    }
