import os
import uuid
import hashlib

from flask import Flask, request, abort, send_file, session
import pymysql
from pymysql.constants import CLIENT

FILE_SAVE_PATH = './image'

def connection():
    conn = pymysql.connect(
        host='192.168.2.8',
        user='piggy',
        password='123456',
        database='photohub',
        client_flag=CLIENT.MULTI_STATEMENTS,
        autocommit=True,
    )
    return conn

app = Flask(__name__, static_url_path='')
app.secret_key = 'photohubxstdgmhjxvsptbpzvgzxfnvqv'

@app.cli.command("init")
def init():
    with connection().cursor() as cur:
        init_sql = open('db.sql').read()
        cur.execute(init_sql)

    os.makedirs(FILE_SAVE_PATH, exist_ok=True)

@app.get('/')
def index():
    return app.send_static_file('index.html')

import user
import upload
import image
import photos
import share
import category
import edit

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
