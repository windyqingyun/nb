from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask import Flask,render_template
from flask_bootstrap import Bootstrap

class NameForm(FlaskForm):
    name = StringField('name',validators=[Required()])
    submit = SubmitField('submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gaa'
bootstrap = Bootstrap(app)

@app.route('/index',methods=['POST','GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
         name = form.name.data
         print name
    return render_template('test2.html',form=form)

app.run(host='0.0.0.0')
