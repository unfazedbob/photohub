from flask import request, abort, send_file, session

from db import connection

# /api/photos
# 当前用户的全部照片
def all_photo():
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    search_query = request.args.get('q')
    category_query = request.args.get('cat')

    with connection().cursor() as cur:
        sql = '''
        SELECT id, owner_id, filename, category, comment 
        FROM photo 
        WHERE owner_id = %s
        '''
        params = [int(session['user_id'])]

        if search_query:
            sql += ' AND comment LIKE %s'
            params.append(f'%{search_query}%')

        if category_query and category_query != '':
            sql += ' AND category = %s'
            params.append(category_query)

        cur.execute(sql, params)

        data = []
        for (id, owner_id, filename, category, comment) in cur.fetchall():
            data.append({
                'id': id,
                'owner_id': owner_id,
                'url': f'/api/image/{filename}',
                'category': category,
                'comment': comment,
            })
        return {
            'ok': True,
            'photos': data,
        }

# /api/photo/<id>
def single_photo(id):
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
        sql = 'SELECT id, owner_id, filename, category, comment FROM photo WHERE owner_id = %s AND id = %s'
        cur.execute(sql, (int(session['user_id']), photo_id))
        (id, owner_id, filename, category, comment) = cur.fetchone()
        return {
            'ok': True,
            'data': {
                'id': id,
                'owner_id': owner_id,
                'url': f'/api/image/{filename}',
                'category': category,
                'comment': comment,
            },
        }

# /api/photo/<id>/update
def update_photo(id):
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
        sql = '''
        UPDATE photo
        SET comment = %s, category = %s
        WHERE owner_id = %s AND id = %s
        '''
        cur.execute(sql, (
            request.form['comment'],
            request.form['category'],
            int(session['user_id']),
            photo_id,
        ))
        sql = 'SELECT id, owner_id, filename, category, comment FROM photo WHERE owner_id = %s AND id = %s'
        cur.execute(sql, (int(session['user_id']), photo_id))
        (id, owner_id, filename, category, comment) = cur.fetchone()
        return {
            'ok': True,
            'data': {
                'id': id,
                'owner_id': owner_id,
                'url': f'/api/image/{filename}',
                'category': category,
                'comment': comment,
            },
        }
