# Web App for MCDA5570-Assignment02
# By: macdre

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from gensim.models import word2vec
import logging
import urllib
import zipfile

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
sentences = None

def background_thread():

    testfile = urllib.URLopener()
    socketio.emit('my_response', {'data': 'Downloading text8 file', 'count': 'n/a'}, namespace='/test')
    testfile.retrieve("http://mattmahoney.net/dc/text8.zip", "/tmp/text8.zip")
    socketio.emit('my_response', {'data': 'Download complete text8 file', 'count': 'n/a'}, namespace='/test')    
    socketio.emit('my_response', {'data': 'Extracting text8 file', 'count': 'n/a'}, namespace='/test')
    #zip_ref = zipfile.ZipFile('/tmp/text8.zip', 'r')
    #zip_ref.extractall('/tmp')
    #zip_ref.close()
    socketio.emit('my_response', {'data': 'Extract complete text8 file', 'count': 'n/a'}, namespace='/test')
    socketio.emit('my_response', {'data': 'Loading word2vec', 'count': 'n/a'}, namespace='/test')
    #sentences = word2vec.Text8Corpus('/tmp/text8')
    #model = word2vec.Word2Vec(sentences, size=200)
    socketio.emit('my_response', {'data': 'Load Complete', 'count': 'n/a'}, namespace='/test')


def background_thread_old():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')
         
@app.route('/')
def index(): 
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/hello')
def hello():
    return 'Hello there! Just moosing around'

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
    
if __name__ == "__main__":
    socketio.run(app)