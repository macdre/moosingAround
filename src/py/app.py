# Web App implementation of Word2Vec
# By: macdre


from flask import Flask
from gensim.models import word2vec, KeyedVectors
from pathlib import Path
from threading import Thread
from requests import get
#from OpenSSL import SSL
#from werkzeug.serving import run_simple
#import ssl
import connexion
import zipfile
import logging


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


class Word2VecModel(Thread):
    def prepare_corpus(self):
        logging.info("Preparing corpus")
        # Set the corpus path
        corpus_path = Path("./text8")
        # Check to see if we have the corpus already downloaded and extracted
        if not corpus_path.is_file(): 
            # Corpus is not extracted. Set the corpus zip path
            corpus_zip_path = Path("./text8.zip")
            # Check to see if we have the zip file downloaded
            if not corpus_zip_path.is_file():
                # Zip file is not downloaded, inform the client, TODO: probably convert this to a log instead, client doesnt care
                # socketio.emit('my_response', {'data': 'Downloading text8 file', 'count': 'n/a'}, namespace='/test')
                # Download the corpus zip, TODO: can we use the corpus_zip_path object instead of the text here again?
                download("http://mattmahoney.net/dc/text8.zip", "./text8.zip")
                # Download complete, TODO: probably convert to a log instead
                # socketio.emit('my_response', {'data': 'Download complete text8 file', 'count': 'n/a'}, namespace='/test')
            # We have the zip but no corpus, extract it. TODO: probably convert this to a log message    
            # socketio.emit('my_response', {'data': 'Extracting text8 file', 'count': 'n/a'}, namespace='/test')
            # Extract file
            zip_ref = zipfile.ZipFile('./text8.zip', 'r')
            zip_ref.extractall('./')
            zip_ref.close()
            # Extract complete, TODO: convert to a log, client doesnt care about this
            # socketio.emit('my_response', {'data': 'Extract complete text8 file', 'count': 'n/a'}, namespace='/test')        
        

    def configure_model(self): 
        logging.info("Configuring model")  
        global model          
        # Set the model path
        model_path = Path("./text.model.bin")
        # Check to see if we have the model saved
        if not model_path.is_file():
            # Model is not saved, lets create it and save it
            # socketio.emit('my_response', {'data': 'Loading word2vec', 'count': 'n/a'}, namespace='/test')
            sentences = word2vec.Text8Corpus('./text8')
            model = word2vec.Word2Vec(sentences, size=200)
            # socketio.emit('my_response', {'data': 'Load Complete', 'count': 'n/a'}, namespace='/test')
            # Save the model
            model.wv.save_word2vec_format('./text.model.bin', binary=True)
        else:
            # Model is saved, lets load it instead of creating it from scratch again
            # TODO: can we replace the text with the path object?
            model = KeyedVectors.load_word2vec_format('./text.model.bin', binary=True)

    def run(self):
        logging.info("Initializing model")
        self.prepare_corpus()
        self.configure_model()
        logging.info("Model initialization complete!")


def get_result(words):
    adds = []
    subs = []
    for word in words:
        if word['operation']:
            adds.append(word['content'].lower())
        else:
            subs.append(word['content'].lower())
    predicted = model.most_similar(positive=adds, negative=subs, topn=1)
    return(predicted[0][0])
    

def test(name):
    return(name)


global model
model = None
global thread
thread = Thread()
app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml')
application = app.app
logging.basicConfig(filename='info.log',level=logging.INFO)
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('./myserver.key')
#context.use_certificate_file('./myserver.crt')
context = ('./myserver.crt', './myserver.key')


if not thread.isAlive():
    logging.info("Starting thread")
    thread = Word2VecModel()
    thread.start()


if __name__ == "__main__":
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #context.load_cert_chain(certfile="./myserver.crt", keyfile="./myserver.key")
    context = ('./myserver.crt', './myserver.key')
    app.run(threading=True, ssl_context=context)
    #run_simple('localhost', 8080, app, use_reloader=True, threaded=True, ssl_context=context)
