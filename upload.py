import os
import uuid
import hashlib
from flask import request, session, redirect

from db import connection
from config import FILE_SAVE_PATH

# /api/upload
def upload():
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    # 获取上传的文件
    f = request.files['file']
    # 获取文件扩展名
    ext = f.filename.rsplit('.', 1)[-1]
    # 生成唯一的文件名
    filename = uuid.uuid4().hex + '.' + ext
    # 生成文件保存路径
    path = os.path.join(FILE_SAVE_PATH, filename)
    # 保存文件
    f.save(path)

    # 获取当前登录用户的ID
    owner_id = int(session['user_id'])

    # 连接数据库并插入新上传的文件信息
    with connection().cursor() as cur:
        sql = 'INSERT INTO photo (owner_id, filename) VALUES (%s, %s)'
        cur.execute(sql, (owner_id, filename))
        
        # 重定向到编辑页面，并传递新插入记录的ID
        return redirect(f'/edit.html?id={cur.lastrowid}')
