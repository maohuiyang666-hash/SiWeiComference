from app.sqlConnect import Mssql
from . import home
from flask import render_template, url_for, redirect, flash, session, request
import uuid  # 添加唯一标志符
from app import app
from werkzeug.security import generate_password_hash
from functools import wraps  # 装饰器(用于访问控制)
from werkzeug.utils import secure_filename
import os, stat, datetime
from math import ceil
from app import process
import random,time,re
import os
from pypinyin import lazy_pinyin


import chardet
import math

model1=process.DataProcess()



def change_filename(filename):
    # fileinfo = os.path.splitext(filename)  # 取出上传的文件名的后缀(.MP4)
    fileinfo = filename.split('.')  # 取出上传的文件名的后缀(.MP4)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + '.' + fileinfo[-1]
    return filename



# 首页
@home.route('/', methods = ['GET', 'POST'])
def index():
    db = Mssql()
    sql_notice = 'select top 5 * from notice order by notice_time desc'
    notices = db.getItems(sql_notice)
    sql_con = 'select top 5 * from conference order by con_time desc'
    cons = db.getItems(sql_con)
    # print(notices)
    return render_template('home/index.html', notices = notices, cons = cons)



# 公告列表
@home.route('/notice_list', methods = ['GET', 'POST'])
def notice_list():
    return render_template('home/list.html')



# 公告详情页
@home.route('/notice_detail', methods = ['GET', 'POST'])
def notice_detail():
    notice_id = int(request.args.get('id',0))
    if notice_id:
        db = Mssql()
        sql_notice = f'select * from notice where notice_id ={int(notice_id)}'
        con = db.getItems(sql_notice)
        print(con)
        if con != []:
            title = con[0][1]
            if con[0][2]:
                content = con[0][2].replace('\n', '|').replace('\r', '|')
                # print(content)
                data = content.split('||')
                # print(data)
            else:
                data = '暂无内容'

            return render_template('home/notice_detail.html', title = title, content = data)
        else:
            return "页面不存在"



# 会议列表
@home.route('/conference/<int:page>/', methods = ['GET'])
def conference(page=None):
    db = Mssql()
    # conference中所有会议
    con_all = db.getItems('select * from conference')
    all = len(con_all)
    # print(all)
    
    # 分页，每页10条
    page_number = 10
    # 分的页数
    page_all = ceil(all / page_number)
    # print(page_all)
    if page == None:
        page = 1
    #当前页的数据 
    con_number = page_number * (page - 1)
    sql_conference = f'select top {page_number} * from conference where con_id not in(select top {con_number} con_id from conference order by con_time desc) order by con_time desc'
    # print(sql_conference)
    con = db.getItems(sql_conference)
    # print(con)
    return render_template('home/conference.html', page_all = page_all, con=con)



# 会议详情页
@home.route('/conference_detail', methods=['GET', 'POST'])
def conference_detail():
    con_id = int(request.args.get('id',0))
    if con_id:
        db = Mssql()
        sql_conference = f'select * from conference where con_id ={int(con_id)}'
        con = db.getItems(sql_conference)
        # print(con)
        if con != []:
            title = con[0][1]
            if con[0][2] == None:
                data = '暂无内容'
            else:
                content = con[0][2].replace('\n', '|').replace('\r', '|')
                # print(content)
                data = content.split('||')
                # print(data)
        # 论文投稿
        if request.method == 'POST':
            f = request.files.get('fileupload')
            print(f)
            basepath = os.path.dirname(__file__)
            if f:
                filename = secure_filename(''.join(lazy_pinyin(f.filename)))
                filename = change_filename(filename)
                print(filename)
                uploadpath = os.path.join(basepath, 'uploads/', filename)
                print(uploadpath)
                f.save(uploadpath)
                flash('文件上传成功!', 'success')
            else:
                flash('还未选择文件', 'danger')
            return redirect(url_for('home.index'))

        return render_template('home/conference_detail.html',con_id=con_id , title=title, content=data)
    else:
        return "页面不存在"
        
        
#会议议程
@home.route('/conference_procedure', methods=['GET', 'POST'])
def conference_procedure():
    con_id = int(request.args.get('id',0))
    if con_id:
        db = Mssql()
        sql_conference = f'select * from conference where con_id ={int(con_id)}'
        con = db.getItems(sql_conference)
        # print(con)
        if con != []:
            title = con[0][1]
            if con[0][5] == None:
                data = '暂无内容'
            else:
                content = con[0][5].replace('\n', '|').replace('\r', '|')
                # print(content)
                data = content.split('||')
                # print(data)
        return render_template('home/conference_procedure.html', con_id=con_id ,title=title, content=data)
    else:
        return "页面不存在"

#会议嘉宾
@home.route('/conference_vip', methods=['GET', 'POST'])
def conference_vip():
    con_id = int(request.args.get('id',0))
    if con_id:
        db = Mssql()
        sql_conference = f'select * from con_vip where con_id ={int(con_id)}'
        con = db.getItems(sql_conference)
        # print(con)
        # print(con[0][5])
        return render_template('home/conference_vip.html', con = con)
    else:
        return "页面不存在"

# 协会简介
@home.route('/swkx', methods=['GET', 'POST'])
def swkx():
    return render_template('home/swkx.html')


@home.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('home/rules.html')


# 协会领导
@home.route('/leader', methods=['GET', 'POST'])
def leadersInfo():
    db = Mssql()
    sql_leader = 'select * from leaders'
    leaders = db.getItems(sql_leader)
    # print(leaders)
    return render_template('home/leadersInfo.html', leaders=leaders)


@home.route('/model_test', methods = ['GET', 'POST'])
def model_test():
    return render_template('home/index-model.html')


@home.route('/class_detail/<int:page>-<model_class>', methods = ['GET', 'POST'])
def class_detail(page, model_class):
    models = model()
    start = (page - 1) * 5#起始数据
    row = models.find(model_class, start, 5)
    #统计模型总数
    num = math.ceil(models.find_count(model_class) / 5)#总页数
    return render_template('home/class_detail.html', rows = row, model_class = model_class, num = num, page = page)


@home.route('/model_detail/<int:model_id>', methods = ['GET', 'POST'])
def model_detail(model_id):
    models = model()
    m_id = model_id
    row = models.find_model_detail(m_id)
    return render_template('home/model_detail.html', rows = row)

@home.route('/model_search/page/<int:page>', methods = ['GET', 'POST'])
def model_search(page):
    keyword1 = request.args.get('keyword1')
    keyword2 = request.args.get('keyword2')
    start = (page - 1) * 2#起始数据
    models = model()
    row = models.find_limit(keyword1, keyword2, start, 2)
    #统计模型总数
    num = math.ceil(models.find_limit_count(keyword1, keyword2) / 2)#总页数
    return render_template('home/model_search.html', rows = row, num = num, page = page, keyword1 = keyword1, keyword2 = keyword2)


# 联系我们
@home.route('/contact', methods=['GET', 'POST'])
def contactUs():
    return render_template('home/contactUs.html')



@app.route('/userget',methods=["GET","POST"])
def userget():
    if session.get('username') == None:
        username = ''
    else:

        username = session.get("username")
    print("userget: ",username)
    return username



#跨域
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


#登陆
@home.route('/login',methods=['POST','GET'])
def login():
    session['lastaction'] = 'login'
    # session.permanent = True
    if request.method=='GET':
        return render_template("home/login.html")

    data = {'username':request.form['username'],
            'password': request.form['password']
            }
    print('login',data)
    if model1.loginCheck(data):
        session["username"]=data.get('username')
        return 'success'
    elif model.loginCheck(data,key='email'):
        session["username"] = model.getInfo(data['username'],['username'],key='email')['username']
        return session["username"]
        # return redirect(url_for('home.index',username=session["username"]))
    else:
        return 'error'

#注册
@home.route('/register',methods=['POST','GET'])
def register():
    session['lastaction']='register'
    if request.method=="GET":
        return render_template("home/register.html")


    data = {'username': request.form['username'],
            'password': request.form['password'],
            'email':request.form['email']
            }
    print('register',data)

    if re.search('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$',data['email'])==None:
        return '邮箱格式不正确'
    for k in data:
        if k=='password':continue
        if data[k]==None:
            return '{}不能为空'.format(k)
        if not model.existCheck({k:data[k]}):
            return '{}已被注册'.format(k)
    if model1.register(data):
        return 'success'
    else:
        return '执行错误'


#删除session，重新登陆
@home.route('/deletesession',methods=['POST','GET'])
def deletesession():
    session.clear()#清除session
    return redirect('/')

#修改个人信息
@home.route('/infochange',methods=['POST','GET'])
def infochange():
    session['lastaction'] = 'infochange'
    if session.get('username') == None:
        return redirect(url_for('home.login'))
    if request.method=="GET":
        return render_template("home/infochange.html")

    kewwords={'username':0,'email':0,'member_type':2,'phone':1,'name':1,'birthday':1,'organization':1,'title':1}
    verifys = {'phone':"verify.verifyPhone()", 'name':"verify.verifyName()", 'member_type':"verify.verifyType()",
               'birthday':"verify.verifyBirthday()", 'organization':"verify.verifyOrganization()", 'title':"verify.verifyTitle()"}
    name_transfor = {'username': '用户名', 'email': '邮箱', 'name': '姓名', 'phone': '电话', 'member_type': '会员类型',
                     'birthday': '生日', 'organization':'单位','title':'职称'}
    data = {'username':session.get('username')
            }
    print('infochange',data)
    result=model1.infoChange(data,kewwords,name_transfor,verifys)
    # print(result)
    return result

# 修改密码
@home.route('/pwchange', methods=['POST', 'GET'])
def pwchange():
    session['lastaction'] = 'pwchange'
    if request.method == "GET":
        return render_template("home/pwchange.html",info={'username':session.get('username')})


#检查用户名/邮箱/电话等是否已经注册
@home.route('/exist_check',methods=['POST','GET'])
def exist_check():
    data=dict(request.form)
    print(data)
    if model1.existCheck(data):
        return 'success'
    else:
        return 'error'

#更新单个个人信息
@home.route('/update',methods=['POST','GET'])
def update_data():
    if session.get('username') == None:
        return redirect(url_for('home.login'))
    data = dict(request.values)
    data['username']=session.get('username')
    print('update',data)
    if 'phone' in data:
        s='((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)'
        if re.search(s,data['phone']) ==None:
            return '电话格式错误'
    if model1.updateInfo(data):
        return 'success'
    else:
        return '修改失败'

#邮箱验证码
@home.route('/verifycode',methods=['POST','GET'])
def verifycode():
    session['lastaction'] = 'pwchange'
    print('verifycode',request.values)
    if request.values.get("state")=='send':
        now=time.time()
        if session.get('time')!=None and now-session.get('time')<60:
            return '操作太频繁，请稍后再试'
        session['time']=now
        email=request.values.get("email")
        # if model.existCheck({"email":email}):
        #     return '邮箱不存在'
        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        session['verifycode']=code
        model1.sendEmail([request.values.get("email")],'你的验证码是'+code+'，请不要告诉别人哦')
        return 'success'
    else:
        if session['verifycode']==request.values.get("code"):
            data={'email':request.values.get("email"),
                  'password':request.values.get("password")}
            print(data)
            if model1.updateInfo(data,key='email'):
                return 'success'
            else:
                return '执行错误'
        else:
            return '验证码错误'



@home.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('fileupload')
        basepath = os.path.dirname(__file__)
        if f:
            filename = secure_filename(f.filename)
            uploadpath = os.path.join(basepath, 'uploads/', filename)
            print(uploadpath)
            f.save(uploadpath)
            flash('文件上传成功!', 'success')
        else:
            flash('还未选择文件', 'danger')
        return redirect(url_for('home.upload'))
    return render_template('home/detail.html')