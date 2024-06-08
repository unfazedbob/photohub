import os
import uuid
import hashlib
from flask import request, session, redirect

from db import connection
from config import FILE_SAVE_PATH

# /api/upload
def upload():
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    f = request.files['file']
    ext = f.filename.rsplit('.', 1)[-1]
    filename = uuid.uuid4().hex + '.' + ext
    path = os.path.join(FILE_SAVE_PATH, filename)
    f.save(path)

    owner_id = int(session['user_id'])

    with connection().cursor() as cur:
        sql = 'INSERT INTO photo (owner_id, filename) VALUES (%s, %s)'
        cur.execute(sql, (owner_id, filename))
        
        return redirect(f'/edit.html?id={cur.lastrowid}')
