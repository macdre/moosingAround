# Web App implementation of Word2Vec
# By: macdre

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from gensim.models import word2vec, KeyedVectors
from requests import get
from pathlib import Path
import eventlet
import logging
import zipfile
import _thread

eventlet.monkey_patch()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

async_mode = 'eventlet'
socketio = SocketIO(app, async_mode=async_mode)
thread01 = None
# thread02 = None
model = None

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


def initialize_model():
    prepare_corpus()
    configure_model()
    
def prepare_corpus():
    # Set the corpus path
    corpus_path = Path("/tmp/text8")
    # Check to see if we have the corpus already downloaded and extracted
    if not corpus_path.is_file(): 
        # Corpus is not extracted. Set the corpus zip path
        corpus_zip_path = Path("/tmp/text8.zip")
        # Check to see if we have the zip file downloaded
        if not corpus_zip_path.is_file():
            # Zip file is not downloaded, inform the client, TODO: probably convert this to a log instead, client doesnt care
            socketio.emit('my_response', {'data': 'Downloading text8 file', 'count': 'n/a'}, namespace='/test')
            # Download the corpus zip, TODO: can we use the corpus_zip_path object instead of the text here again?
            download("http://mattmahoney.net/dc/text8.zip", "/tmp/text8.zip")
            # Download complete, TODO: probably convert to a log instead
            socketio.emit('my_response', {'data': 'Download complete text8 file', 'count': 'n/a'}, namespace='/test')
        # We have the zip but no corpus, extract it. TODO: probably convert this to a log message    
        socketio.emit('my_response', {'data': 'Extracting text8 file', 'count': 'n/a'}, namespace='/test')
        # Extract file
        zip_ref = zipfile.ZipFile('/tmp/text8.zip', 'r')
        zip_ref.extractall('/tmp')
        zip_ref.close()
        # Extract complete, TODO: convert to a log, client doesnt care about this
        socketio.emit('my_response', {'data': 'Extract complete text8 file', 'count': 'n/a'}, namespace='/test')        
    

def configure_model(): 
    global model
    # Set the model path
    model_path = Path("/tmp/text.model.bin")
    # Check to see if we have the model saved
    if not model_path.is_file():
        # Model is not saved, lets create it and save it
        socketio.emit('my_response', {'data': 'Loading word2vec', 'count': 'n/a'}, namespace='/test')
        sentences = word2vec.Text8Corpus('/tmp/text8')
        model = word2vec.Word2Vec(sentences, size=200)
        socketio.emit('my_response', {'data': 'Load Complete', 'count': 'n/a'}, namespace='/test')
        # Save the model
        model.wv.save_word2vec_format('/tmp/text.model.bin', binary=True)
    else:
        # Model is saved, lets load it instead of creating it from scratch again
        # TODO: can we replace the text with the path object?
        model = KeyedVectors.load_word2vec_format('/tmp/text.model.bin', binary=True)


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')


@app.route('/')
def index(): 
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('compute_event', namespace='/test')
def compute_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    predicted = model.most_similar(positive=message['add_data'], negative=message['sub_data'], topn=1)
    emit('compute_response',
         {'data': predicted[0][0], 'count': session['receive_count']})


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread01
#    global thread02            
#    if thread02 is None:
#        thread02 = socketio.start_background_task(target=background_thread)
#    emit('my_response', {'data': 'Connected', 'count': 0})
    if thread01 is None:
        thread01 = 1
        eventlet.spawn(initialize_model)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
    
    
if __name__ == "__main__":
    socketio.run(app)