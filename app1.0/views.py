from flask import render_template,redirect,flash,url_for,request,session,jsonify
from .model import User,Blog
from .form import LoginForm,RegisterForm
import json
from .tools import get_md5,get_uuid,get_current_time
from . import main


@main.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()


    existAccount = session.get('account',None)

    if existAccount is not None: 
        
        blogs = Blog().findByAccountLimit(existAccount)
        blogArr = []
        for blog in blogs:
            blogArr.append(blog)
       
        return render_template('home.html',blogs=blogArr)

    form = LoginForm()

    if form.validate_on_submit():
        user = User(form.account.data.strip(),get_md5(form.password.data))

        result = user.find()

        if result is None :
            flash("wrong account or password!")
            return redirect(url_for("main.index"))
        else :
            session['account'] = user.account
        
            blogs = Blog().findByAccountLimit(user.account)
            blogArr = []
            for blog in blogs:
                blogArr.append(blog)
            return render_template('home.html',blogs=blogArr)

    return render_template("login.html",form=form)


@main.route('/register',methods=['GET','POST'])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        account = form.account.data.strip()	
        password = get_md5(form.password.data)
	
        user = User(account,password)	
        result = user.findAccount()
    
        if result is  None:
            user.save()
            flash('register success!')
        else:
            flash('Account is exist!')
            return redirect(url_for("main.register"))
        return redirect(url_for('main.index'))

    return render_template('register.html',form=form)

@main.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('account',None)
    return redirect(url_for('main.index'))

@main.route('/writeBlog',methods=['GET','POST'])
def writeBlog():
    return render_template("writeBlog.html")


@main.route('/about',methods=['GET','POST'])
def about():
    return render_template("about.html")


@main.route('/post',methods=['GET','POST'])
def post():
    return render_template("post.html")


@main.route('/saveBlog',methods=['GET','POST'])
def saveBlog():

    uid = get_uuid()
    data = request.form
    title = data['title']
    content = data['content']
    account = session['account']
    currentTime = get_current_time().strftime('%Y-%m-%d %H:%M:%S')
    #currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
     

    blog = Blog(uid,account,title,content,currentTime)
 
    blog.save()

    return redirect(url_for("main.index"))

@main.route('/showBlog/<uid>/',methods=['GET','POST'])
def showBlog(uid):
    
   # uid = request.args['uid']
    
    if uid is None:
        return redirect(url_for('main.index'))
    else :
        blog = Blog().findById(uid)
        return render_template('showBlog.html',blog=blog)
    
    
