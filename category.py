from flask import request, session
from db import connection

# /api/category
def get_categories():
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    with connection().cursor() as cur:
        sql = '''
        SELECT DISTINCT category
        FROM photo
        WHERE owner_id = %s
        '''
        cur.execute(sql, (int(session['user_id']),))

        categories = [row[0] for row in cur.fetchall()]

        return {
            'ok': True,
            'categories': categories,
        }
