# coding=utf-8

from flask import render_template,redirect,flash,url_for,session,jsonify
from .model import User,Blog
from .form import LoginForm,RegisterForm
import json
from .tools import get_md5,get_uuid,get_current_time,cut_string
from . import main
from flask import request, make_response
import hashlib
from dispatcher import MsgDispatcher

import sys

reload(sys)
sys.setdefaultencoding('utf8')


@main.route('/home',methods=['GET','POST'])
def home():
    blogs = Blog().findAll()
    blogArr = []
    
    for blog in blogs:
        blogArr.append(blog)

    return render_template('home.html',blogs=blogArr)


@main.route('/getUser', methods=['GET', 'POST'])
def get_user():
    data = request.form
    request.get_json()
    return jsonify({"name":"zhangsan","age":"2222"})


@main.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User(form.account.data.strip(),get_md5(form.password.data))
        
        result = user.find()

        if result is None :
            flash("wrong account or password!")
            return redirect(url_for("main.login"))
        else:
            session['account'] = user.account
        
            blogs = Blog().findByAccount(user.account)
            blogArr = []
            
            for blog in blogs:
                blogArr.append(blog)

            return render_template('home.html',blogs=blogArr)

    return render_template("login.html", form=form)

@main.route('/',methods=['GET','POST'])
def index():
    existAccount = session.get('account')
    if existAccount is not None: 
        
        blogs = Blog().findByAccount(existAccount)
        blogArr = []
        for blog in blogs:
            blogArr.append(blog)
       
        return render_template('home.html',blogs=blogArr)

    else :
        blogs = Blog().findAll()
        blogArr = []
        for blog in blogs:
            blogArr.append(blog)

        return render_template('home.html',blogs=blogArr)


@main.route('/register',methods=['GET','POST'])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        account = form.account.data.strip()	
        password = get_md5(form.password.data)
        user = User(account, password)
        result = user.findAccount()
    
        if result is  None:
            user.save()
            flash('Register success!')
        else:
            flash('Account is exist!')
            return redirect(url_for("main.register"))
        return redirect(url_for('main.login'))

    return render_template('register.html',form=form)

@main.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('account',None)
    return redirect(url_for('main.index'))

@main.route('/writeBlog',methods=['GET','POST'])
def writeBlog():
    
    existAccount = session.get('account',None)
    
    if existAccount is None:
        return redirect(url_for('main.login'))
    else:
        return render_template("writeBlog.html")


@main.route('/about',methods=['GET','POST'])
def about():
    return render_template("about.html")


@main.route('/post',methods=['GET','POST'])
def post():
    return render_template("post.html")


@main.route('/saveBlog',methods=['POST'])
def saveBlog():

    uid = get_uuid()
    data = request.form
    title = data['title']
    content = data['content']
    contentTxt = cut_string(data['contentTxt'],200)
    account = session['account']
    currentTime = get_current_time().strftime('%Y-%m-%d %H:%M:%S')

    blog = Blog(uid,account,title,content,contentTxt,currentTime)
    blog.save()

    return redirect(url_for("main.index"))

@main.route('/showBlog/<uid>',methods=['GET','POST'])
def showBlog(uid):
    print 111111
    if uid is None:
        return redirect(url_for('main.index'))
    else :
        blog = Blog().findById(uid)
        return render_template('showBlog.html',blog=blog)
    
    
@main.route('/deleteBlog/<uid>',methods=['GET','POST'])
def deleteBlog(uid):
    
    existAccount = session.get('account',None)
    blog = Blog().findById(uid)
    if blog['account'] == existAccount :
        Blog().deleteById(uid)
        flash('delete success')
    else :
        flash('you dont have this permission!!!')

    return redirect(url_for('main.index'))


@main.route('/more',methods=['POST'])
def moreBlog():    
    path = request.form['path']
    page =  int(request.form['page']) 
    existAccount = session.get('account',None)
      
    if path == '/home' or existAccount is None:
        blogs = Blog().findAll(page)
    else:
        blogs = Blog().findByAccount(existAccount,page)

    blogArr = []
    for blog in blogs:
        blogArr.append(json.dumps(blog))

    return jsonify(blogArr)


@main.route('/wx', methods=['GET', 'POST'])
def wechat_auth():  # 处理微信请求的处理函数，get方法用于认证，post方法取得微信转发的数据
    if request.method == 'GET':
        token = 'nanshao'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)

        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()  # 接收消息
        try:
            rec = rec.decode('utf-8')
        except Exception as e:
            rec = rec.decode('gb18030', errors='ignore')

        dispatcher = MsgDispatcher(rec)
        data = dispatcher.dispatch()
        with open("./debug.log", "a") as file:
            file.write(data)
            file.close()
        response = make_response(data)
        response.content_type = 'application/xml'
        return response


@main.route('/order/pay_notify', methods=['POST'])
def pay_notify():
    """
    支付宝支付后回调接口  创建订单
    :return:
    """

    data = request.form
    for key in data:
        print(key, data[key])

    return 'success'

@main.route('/getStatus',methods=['POST','GET'])
def get_status():
    return '2';