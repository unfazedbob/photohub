from flask import request, abort, send_file, session

from db import connection

# /api/photos
# 获取当前用户的全部照片
def all_photo():
    # 检查用户是否登录
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    # 获取查询参数
    search_query = request.args.get('q')
    category_query = request.args.get('cat')

    with connection().cursor() as cur:
        # 构建SQL查询语句
        sql = '''
        SELECT id, owner_id, filename, category, comment 
        FROM photo 
        WHERE owner_id = %s
        '''
        params = [int(session['user_id'])]

        # 如果存在搜索查询，添加到SQL语句中
        if search_query:
            sql += ' AND comment LIKE %s'
            params.append(f'%{search_query}%')

        # 如果存在分类查询，添加到SQL语句中
        if category_query and category_query != '':
            sql += ' AND category = %s'
            params.append(category_query)

        # 执行SQL查询
        cur.execute(sql, params)

        data = []
        # 获取查询结果并格式化
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
# 获取单张照片信息
def single_photo(id):
    # 检查用户是否登录
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
        # 构建SQL查询语句
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
# 更新单张照片信息
def update_photo(id):
    # 检查用户是否登录
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
        # 构建SQL更新语句
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
        # 构建SQL查询语句
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
