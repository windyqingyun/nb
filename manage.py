from flask_script import Manager,Server
from app import initApp
from config import DevConfig

app = initApp()
manager = Manager(app)
app.config.from_object(DevConfig)

#manager.add_command('server',Server())

#@manager.shell
#def make_shell_context():
#	'''Create a python CLI .
#	return:Default import object .'''
#	return dict(app=app)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)
