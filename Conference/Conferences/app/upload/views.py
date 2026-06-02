from app.sqlConnect import Mssql
from . import home
from flask import render_template, url_for, redirect, flash, session, request
import uuid  # 添加唯一标志符
from app import app
from werkzeug.security import generate_password_hash
from functools import wraps  # 装饰器(用于访问控制)
from werkzeug.utils import secure_filename
import os, stat, datetime
from flask_paginate import Pagination


@home.route('/', methods = ['GET', 'POST'])
def index():
    db = Mssql()
    sql_notice = 'select * from notice'
    notices = db.getItems(sql_notice)
    print(notices)
    return render_template('home/index.html', notices = notices)

# @home.route('/detail', methods = ['GET', 'POST'])
# # 协会简介
# def detail():
#     return render_template('home/detail.html')

# 协会领导
@home.route('/leader', methods = ['GET', 'POST'])
def leadersInfo():
    db = Mssql()
    sql_leader = 'select * from leaders'
    leaders = db.getItems(sql_leader)
    print(leaders)
    return render_template('home/leadersInfo.html', leaders = leaders)

# 联系我们
@home.route('/contact', methods = ['GET', 'POST'])
def contactUs():
    return render_template('home/contactUs.html')


# 上传文件
from flask import Flask, render_template, request, flash, redirect, url_for

import os
from werkzeug.utils import secure_filename

@home.route('/detail', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        f = request.files.get('fileupload')
        basepath = os.path.dirname(__file__)
        if f:
            filename = secure_filename(f.filename)
            uploadpath = os.path.join(basepath, 'uploads/', filename)
            f.save(uploadpath)
            flash('文件上传成功!', 'success')
        else:
            flash('还未选择文件', 'danger')
        return redirect(url_for('home.process'))
    return render_template('home/detail.html')





