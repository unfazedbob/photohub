import os
import uuid
from flask import request, session, abort
from subprocess import run

from db import connection
from config import FILE_SAVE_PATH

# /api/photo/<id>/edit
def edit_photo(id):
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    try:
        # 将照片ID转换为整数
        photo_id = int(id)
    except ValueError:
        # 如果ID不是整数，返回400错误
        abort(400)

    # 获取表单中的cmd参数
    cmd = request.form.get('cmd')
    if not cmd:
        return {
            'ok': False,
            'message': "缺少 cmd 参数"
        }

    with connection().cursor() as cur:
        # 查询数据库中照片的文件名
        sql = 'SELECT filename FROM photo WHERE owner_id = %s AND id = %s'
        cur.execute(sql, (int(session['user_id']), photo_id))
        result = cur.fetchone()
        if not result:
            return {
                'ok': False,
                'message': "照片不存在"
            }

        # 获取旧文件名和路径
        old_filename = result[0]
        old_path = os.path.join(FILE_SAVE_PATH, old_filename)

        # 生成新的文件名
        ext = old_filename.rsplit('.', 1)[-1]
        new_filename = uuid.uuid4().hex + '.' + ext
        new_path = os.path.join(FILE_SAVE_PATH, new_filename)

        # 运行转换命令
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

        # 更新数据库中的文件名
        sql = 'UPDATE photo SET filename = %s WHERE owner_id = %s AND id = %s'
        cur.execute(sql, (new_filename, int(session['user_id']), photo_id))

        # 删除旧文件
        os.remove(old_path)

        return {
            'ok': True,
            'message': "照片编辑成功",
            'data': {
                'id': photo_id,
                'filename': new_filename
            }
        }
