from flask import request, abort, session

from db import connection

# /api/share/<id>
def view_share(id):
    # 打印分享ID、类型和长度
    print(id, type(id), len(id))
    try:
        # 将分享ID转换为整数
        share_id = int(id)
    except ValueError:
        # 如果转换失败，打印错误信息并返回400错误
        print("分享ID不是有效的整数")
        abort(400)

    with connection().cursor() as cur:
        # 查询分享记录，检查密码是否匹配
        sql = 'SELECT photo_id FROM share WHERE id = %s AND password = %s'
        cur.execute(sql, (share_id, request.args.get('password', '')))
        try:
            # 获取查询结果中的照片ID
            (photo_id, ) = cur.fetchone()
        except:
            # 如果查询失败，返回错误信息
            return {
                'ok': False
            }

        # 查询照片文件名
        sql = 'SELECT filename FROM photo WHERE id = %s'
        cur.execute(sql, (photo_id, ))
        (filename, ) = cur.fetchone()
        return {
            'ok': True,
            'data': {
                'filename': filename,
            },
        }

# /api/photo/<id>/share
def share_photo(id):
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
        # 如果转换失败，返回400错误
        abort(400)

    with connection().cursor() as cur:
        # 检查照片是否属于当前登录用户
        sql = 'SELECT 1 FROM photo WHERE id = %s AND owner_id = %s'
        cur.execute(sql, (photo_id, int(session['user_id'])))
        if len(cur.fetchall()) == 0:
            return {
                'ok': False,
            }

        # 插入新的分享记录
        sql = 'INSERT INTO share (photo_id, password) VALUES (%s, %s)'
        cur.execute(sql, (
            photo_id,
            request.form.get('password', None),
        ))
        return {
            'ok': True,
            'share_id': cur.lastrowid
        }
