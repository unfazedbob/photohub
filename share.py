from flask import request, abort, session

from db import connection

# /api/share/<id>
def view_share(id):
    # try:
    print(id, type(id), len(id))
    share_id = int(id)
    # except ValueError:
    #     print("???")
    #     abort(400)

    with connection().cursor() as cur:
        sql = 'SELECT photo_id FROM share WHERE id = %s AND password = %s'
        cur.execute(sql, (share_id, request.args.get('password', '')))
        try:
            (photo_id, ) = cur.fetchone()
        except:
            return {
                'ok': False
            }

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
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }
    try:
        photo_id = int(id)
    except ValueError:
        abort(400)

    with connection().cursor() as cur:
        sql = 'SELECT 1 FROM photo WHERE id = %s AND owner_id = %s'
        cur.execute(sql, (photo_id, int(session['user_id'])))
        if len(cur.fetchall()) == 0:
            return {
                'ok': False,
            }

        sql = 'INSERT INTO share (photo_id, password) VALUES (%s, %s)'
        cur.execute(sql, (
            photo_id,
            request.form.get('password', None),
        ))
        return {
            'ok': True,
            'share_id': cur.lastrowid
        }
