from flask import request, session
from db import connection

# 定义一个处理获取分类的API端点
# /api/category
def get_categories():
    # 检查用户是否已登录，如果没有'user_id'在session中，则返回未登录的错误信息
    if 'user_id' not in session:
        return {
            'ok': False,
            'message': "没有登录"
        }

    # 使用数据库连接创建一个游标对象
    with connection().cursor() as cur:
        # 定义SQL查询语句，选择用户拥有的照片的不同分类
        sql = '''
        SELECT DISTINCT category
        FROM photo
        WHERE owner_id = %s
        '''
        # 执行SQL查询，传入用户的ID作为参数
        cur.execute(sql, (int(session['user_id']),))

        # 获取查询结果，并将每个结果的第一列（分类名称）提取出来
        categories = [row[0] for row in cur.fetchall()]

        # 返回成功信息和分类列表
        return {
            'ok': True,
            'categories': categories,
        }
