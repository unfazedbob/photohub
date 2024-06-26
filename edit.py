import os
import uuid
from flask import request, session, abort
from subprocess import run

from db import connection
from config import FILE_SAVE_PATH

# /api/photo/<id>/edit
def edit_photo(id):
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    try:
        photo_id = int(id)
    except ValueError:
        abort(400)

    cmd = request.form.get('cmd')
    if not cmd:
        return {
            'ok': False,
            'message': "缺少 cmd 参数"
        }

    with connection().cursor() as cur:
        sql = 'SELECT filename FROM photo WHERE owner_id = %s AND id = %s'
        cur.execute(sql, (int(session['user_id']), photo_id))
        result = cur.fetchone()
        if not result:
            return {
                'ok': False,
                'message': "照片不存在"
            }

        old_filename = result[0]
        old_path = os.path.join(FILE_SAVE_PATH, old_filename)

        # Generate a new filename
        ext = old_filename.rsplit('.', 1)[-1]
        new_filename = uuid.uuid4().hex + '.' + ext
        new_path = os.path.join(FILE_SAVE_PATH, new_filename)

        # Run the convert command
        try:
            z = ['convert', old_path]
            z.extend(cmd.split(' '))
            z.append(new_path)
            run(z, check=True)
        except Exception as e:
            return {
                'ok': False,
                'message': f"处理图像时出错: {str(e)}"
            }

        # Update the database with the new filename
        sql = 'UPDATE photo SET filename = %s WHERE owner_id = %s AND id = %s'
        cur.execute(sql, (new_filename, int(session['user_id']), photo_id))

        # Optionally, remove the old file
        os.remove(old_path)

        return {
            'ok': True,
            'message': "照片编辑成功",
            'data': {
                'id': photo_id,
                'filename': new_filename
            }
        }
