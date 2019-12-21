from flask import Flask
from flask_socketio import SocketIO

def socket_app(*args, **kwargs):
    app = Flask(__name__)
    socketio = SocketIO(app, log_output=True)
    
    @socketio.on('message')
    def handle_message(message):
        print(message)
    # socketio.run(app, host='0.0.0.0', port=5002)
    return app

