from app.sqlConnect import Mssql
from . import home
from flask import render_template, url_for, redirect, flash, session, request
from flask_paginate import Pagination,get_page_parameter
import uuid  # 添加唯一标志符
from app import app
from werkzeug.security import generate_password_hash
from functools import wraps  # 装饰器(用于访问控制)
from werkzeug.utils import secure_filename
import os, stat, datetime


@home.route('/', methods=['GET', 'POST'])
def index():
    db = Mssql()
    sql_notice = 'select * from notice'
    notices = db.getItems(sql_notice)
    print(notices)
    return render_template('home/index.html', notices=notices)


@home.route('/conference', methods=['GET', 'POST'])
def conference():
    per_page=20

    sql_conference = 'select * from conference'
    db = Mssql()
    con = db.getItems(sql_conference)
    print(con)
    return render_template('home/conference.html', con=con)



@home.route('/conference/<con_id>', methods=['GET', 'POST'])
def conference_list(con_id):
    if con_id:
        db = Mssql()
        sql_conference = f'select * from conference where con_id ={int(con_id)}'
        con = db.getItems(sql_conference)
        print(con)
        if con != []:
            title = con[0][1]

            content = con[0][2].replace('\n', '|').replace('\r', '|')
            print(content)
            data = content.split('||')
            print(data)

            return render_template('home/conference_detail.html', title=title, content=data)
        else:
            return "页面不存在"


@home.route('/detail', methods=['GET', 'POST'])
# 协会简介
def detail():
    return render_template('home/detail.html')


# 协会领导
@home.route('/leader', methods=['GET', 'POST'])
def leadersInfo():
    db = Mssql()
    sql_leader = 'select * from leaders'
    leaders = db.getItems(sql_leader)
    print(leaders)
    return render_template('home/leadersInfo.html', leaders=leaders)


# 联系我们
@home.route('/contact', methods=['GET', 'POST'])
def contactUs():
    return render_template('home/contactUs.html')
