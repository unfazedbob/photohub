import os
import uuid
import hashlib

from flask import Flask, request, abort, send_file, session
import pymysql
from pymysql.constants import CLIENT
from db import connection

# 定义文件保存路径
FILE_SAVE_PATH = './image'

# 创建Flask应用实例
app = Flask(__name__, static_url_path='')
# 设置Flask应用的密钥，用于session加密
app.secret_key = 'photohubxstdgmhjxvsptbpzvgzxfnvqv'

# 初始化数据库和文件保存路径的命令
@app.cli.command("init")
def init():
    with connection().cursor() as cur:
        # 读取SQL文件并执行初始化脚本
        init_sql = open('db.sql').read()
        cur.execute(init_sql)

    # 创建文件保存路径，如果已存在则忽略
    os.makedirs(FILE_SAVE_PATH, exist_ok=True)

# 首页路由，返回静态文件
@app.get('/')
def index():
    return app.send_static_file('index.html')

# 导入各个模块的视图函数
import user
import upload
import image
import photos
import share
import category
import edit

# 定义各个API路由和对应的视图函数
app.add_url_rule('/api/user/status', view_func=user.status)
app.add_url_rule('/api/user/register', view_func=user.register, methods=['POST'])
app.add_url_rule('/api/user/login', view_func=user.login, methods=['POST'])
app.add_url_rule('/api/user/logout', view_func=user.logout, methods=['POST'])

app.add_url_rule('/api/upload', view_func=upload.upload, methods=['POST'])
app.add_url_rule('/api/image/<filename>', view_func=image.image)

app.add_url_rule('/api/photos', view_func=photos.all_photo)
app.add_url_rule('/api/photo/<id>', view_func=photos.single_photo)
app.add_url_rule('/api/photo/<id>/update', view_func=photos.update_photo, methods=['POST'])

app.add_url_rule('/api/share/<id>', view_func=share.view_share)
app.add_url_rule('/api/photo/<id>/share', view_func=share.share_photo, methods=['POST'])

app.add_url_rule('/api/category', view_func=category.get_categories)

app.add_url_rule('/api/photo/<id>/edit', view_func=edit.edit_photo, methods=['POST'])
