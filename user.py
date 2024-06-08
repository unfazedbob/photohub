import hashlib

from flask import request, session
import pymysql

from db import connection

# /api/user/status
def status():
    if 'user_id' not in session:
        return {
            'logined': False
        }
    with connection().cursor() as cur:
        sql = 'SELECT username FROM user WHERE id = %s'
        cur.execute(sql, (int(session['user_id'])))
        username = cur.fetchone()[0]
        return {
            'logined': True,
            'username': username,
        }
    
secret_key = 'photohubxstdgmhjxvsptbpzvgzxfnvqv'

# /api/user/register
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = hashlib.blake2b((password + secret_key).encode()).hexdigest()

    with connection().cursor() as cur:
        sql = 'INSERT INTO user (username, password_hash) VALUES (%s, %s)'
        try:
            cur.execute(sql, (username, password_hash))
        except pymysql.err.IntegrityError:
            session.clear()
            return {
                'logined': False,
                'message': '用户名已存在'
            }

        session['user_id'] = cur.lastrowid
        return {
            'logined': True,
            'username': username,
        }

# /api/user/login
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = hashlib.blake2b((password + secret_key).encode()).hexdigest()

    with connection().cursor() as cur:
        sql = 'SELECT id FROM user WHERE username = %s AND password_hash = %s'
        cur.execute(sql, (username, password_hash))
        data = cur.fetchone()
        if data is None:
            return {
                'logined': False,
                'message': '用户名或密码错误'
            }
        
        session['user_id'] = data[0]
        return {
            'logined': True,
            'username': username,
        }

# /api/user/logout
def logout():
    session.clear()
    return {
        'logined': False,
    }
