from flask_socketio import SocketIO

def InitChatService(app):
    io = SocketIO(app);
        
    return io