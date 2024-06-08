import os
import uuid
import hashlib

from flask import Flask, request, abort, send_file, session
import pymysql
from pymysql.constants import CLIENT

from config import FILE_SAVE_PATH

# /api/image/<filename>
def image(filename):
    path = os.path.join(FILE_SAVE_PATH, filename)
    if not os.path.exists(path):
        abort(404)
    return send_file(path)
