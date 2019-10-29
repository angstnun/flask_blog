import os

from flask import Flask

from . import (
    db, auth, home, blog, chatService
)

def create_app(test_config=None):

    staticFolder = os.path.abspath('./flaskr/public/static')
    app = Flask(__name__, root_path="flaskr/public/", static_folder=staticFolder, instance_relative_config=True)
    app.secret_key = "34ae0d71-3cc0-4297-95fd-2ce6801bf605"

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:  
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.register_blueprint(auth.authBlueprint)
    app.register_blueprint(home.homeBlueprint)
    app.register_blueprint(blog.blogBlueprint)
    app.add_url_rule('/', endpoint='index')

    return app

if __name__ == "__main__":
    app = create_app()
    io = chatService.InitChatService(app)
    
    @io.on('connection')
    def OnConnection(json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        
    @io.on('my event')
    def OnMyEvent(json):
        print('received json: ' + str(json))
    
    app.run(port=5000, host=('0.0.0.0'))
    