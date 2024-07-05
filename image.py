import os
import uuid
import hashlib

from flask import Flask, request, abort, send_file, session
import pymysql
from pymysql.constants import CLIENT

from config import FILE_SAVE_PATH

# 定义一个处理图片请求的函数
# /api/image/<filename>
def image(filename):
    # 拼接文件的完整路径
    path = os.path.join(FILE_SAVE_PATH, filename)
    # 检查文件是否存在
    if not os.path.exists(path):
        # 如果文件不存在，返回404错误
        abort(404)
    # 如果文件存在，发送文件
    return send_file(path)
