import pymssql  # 引入pymssql模块
from datetime import datetime
import smtplib,random
from email.mime.text import MIMEText
from app import conf



class DataProcess:
    def __init__(self):

        self.mydb = pymssql.connect(conf.db_host, conf.db_user, conf.db_password, conf.db_database)  # 服务器名,账户,密码,数据库名
        if not self.mydb:
            print("连接失败!")
        self.mycursor = self.mydb.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行

    def reset(self):
        '''重新连接数据库，当更改数据库报错时需执行此函数'''
        self.mycursor.close()  # 关闭游标
        self.mydb.close()  # 关闭连接
        self.mydb = pymssql.connect(conf.db_host, conf.db_user, conf.db_password, conf.db_database)
        self.mycursor = self.mydb.cursor()
        print('have reseted database')

    def loginCheck(self,data,key='username'):
        sql="SELECT * FROM users where {} ='{}' and password='{}'".format(key,data['username'],data['password'])
        self.mycursor.execute(str(sql))
        result = self.mycursor.fetchone()
        return result!=None

    def existCheck(self,data):
        sql = "SELECT * FROM users where "
        keys=list(data)
        for i in range(len(keys)):
            if i>0:
                sql+=" or "
            k=keys[i]
            sql+="{} = '{}'".format(k,data[k])
        print(sql)
        self.mycursor.execute(str(sql))
        result = self.mycursor.fetchone()
        return result == None

    # def infoShow(self,data,columns,name_transfor):
    #     sql="SELECT {} FROM users where username='{}'".format(','.join(columns),data['username'])
    #     print(sql)
    #     self.mycursor.execute(str(sql))
    #     result = self.mycursor.fetchone()
    #     dic={}
    #     for k,v in zip(columns,result):
    #         if v !=None:
    #             dic[k]=v
    #         else:
    #             dic[k]='无'
    #     s='<div class="signup-form" ><label for="{}">{}:</label>' \
    #       '<input type="text" id="{}"  class="email-mobile" value="{}" disabled="disabled" ></div>\n'
    #     result=''
    #     for k in dic:
    #         result+=s.format(k,name_transfor[k],k,dic[k])
    #     print(dic)
    #     return result

    def infoChange(self,data,columns,name_transfor,verifys):
        sql="SELECT {} FROM users where username='{}'".format(','.join(columns),data['username'])
        print(sql)
        self.mycursor.execute(str(sql))
        result = self.mycursor.fetchone()
        dic={}
        for k,v in zip(columns,result):
            if v !=None:
                dic[k]=v
                if k=='birthday':
                    print(str(type(v))=="<class 'datetime.date'>")
                    dic[k]=v.strftime('%Y-%m-%d')
                    print(dic[k])
            else:
                dic[k]='无'

        s1 = '<div class="signup-form" ><label for="{}">{}:</label>' \
            '<input type="text" id="{}"  class="email-mobile" value="{}" disabled=“disabled” ></div>\n'

        s2 = '<div class="signup-form" ><label for="{}" >{}:</label>' \
             '<input type="text" id="{}"  class="email-mobile" value="{}" >' \
             '<a class="in_box" onclick="{}">确认修改</a></div>\n'

        s3 = '<div class="signup-form" ><label for="{}" >{}:</label>' \
             '<input type="text" id="{}"  class="email-mobile" value="{}" >' \
             '<a class="in_box" onclick="{}">修改</a></div>\n'

        result = ''
        for k in columns:
            if columns[k]==0:
                result += s1.format(k, name_transfor[k], k, dic[k])
            elif columns[k]==1:
                result += s2.format(k, name_transfor[k], k, dic[k],verifys[k])
            else:
                result += s3.format(k, name_transfor[k], k, dic[k],verifys[k])
        print(dic)
        return result

    def register(self,data):
        try:
            sql = "INSERT INTO users (username, password,email) VALUES (%s, %s,%s)"
            val = ("{}".format(data['username']), "{}".format(data['password']),"{}".format(data['email']))
            print(sql,val)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            return True
        except:
            self.reset()
            return False

    def updateInfo(self,data,key='username'):
        value=data[key]
        try:
            data.pop(key)
            for k in data:
                assert len(data[k])>0
                sql = "UPDATE  users SET {} = '{}' where {} = '{}'".format(k,data[k],key,value)
                print(sql)
                self.mycursor.execute(sql)
                self.mydb.commit()
            return True
        except:
            self.reset()
            return False

    def getInfo(self,username,columns,key='email'):
        sql = "SELECT {} FROM users where {} = '{}'".format(','.join(columns),key, username)
        print(sql)
        self.mycursor.execute(str(sql))
        result = self.mycursor.fetchone()

        dic={}
        print(result)
        for k, v in zip(columns, result):
            if v == None:
                v = '无'
            elif str(type(v)) == "<class 'datetime.date'>":
                v = v.strftime('%Y-%m-%d')
            dic[k]=v

        return dic

    def sendEmail(self,receivers,msg):
        mail_host = conf.mail_host
        # 163用户名
        mail_user = conf.mail_user
        # 密码(部分邮箱为授权码)
        mail_pass = conf.mail_password
        # 邮件发送方邮箱地址
        sender = conf.main_sender
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        # receivers = ['2405309874@qq.com']

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(msg, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '验证码'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]
        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            # 连接到服务器
            #smtpObj.connect(mail_host, 465)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            return True
        except smtplib.SMTPException as e:
            print('email send error: ', e)  # 打印错误
            return False


def test():
    import pymssql  # 引入pymssql模块
    connect = pymssql.connect(conf.db_host, conf.db_user, conf.db_password, conf.db_database)  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql="select * from users where username = '464' "
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()
    # row = cursor.fetchall()
    print(row)

    # connect.commit()  # 提交
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接



if __name__=='__main__':

    test()

    # model=DataProcess()


    print('end')

#MAERALLJYMJCOUHI






