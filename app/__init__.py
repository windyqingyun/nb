from flask import Flask,Blueprint
from flask_moment import Moment
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
moment = Moment()
main=Blueprint('main',__name__)

app = Flask(__name__)

def initApp():

    bootstrap.init_app(app)
    moment.init_app(app)
 
    app.register_blueprint(main)	

    return app



@app.template_filter('cdot')
def cdot_template_filter(s,lens):
    slen = len(s)
    if slen <= lens:
        return s
    else :
        return s[0:lens]+"..."







from . import views,error,model
