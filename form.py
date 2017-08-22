from flask import Flask,render_template,redirect
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you try'

@app.route("/")
def index():
	return render_template('submit.html')

@app.route('/submit',methods=('GET','POST'))
def submit():
	form = MyForm()
	if form.validate_on_submit():
		print 'aaaa'
		return redirect('/')
	return render_template('hello.html',form=form)

class MyForm(FlaskForm):
	name = TextField('name',validators=[DataRequired()])


if __name__ == '__main__':
	app.run(host='0.0.0.0')


