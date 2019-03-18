# Web App implementation of Word2Vec
# By: macdre


from flask import Flask
from gensim.models import word2vec, KeyedVectors
from pathlib import Path
from threading import Thread
from requests import get
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
                # Download the corpus zip, TODO: can we use the corpus_zip_path object instead of the text here again?
                download("http://mattmahoney.net/dc/text8.zip", "./text8.zip")
                # Download complete, TODO: probably convert to a log instead
            # We have the zip but no corpus, extract it. TODO: probably convert this to a log message    
            # Extract file
            zip_ref = zipfile.ZipFile('./text8.zip', 'r')
            zip_ref.extractall('./')
            zip_ref.close()
            # Extract complete, TODO: convert to a log, client doesnt care about this
        

    def configure_model(self): 
        logging.info("Configuring model")  
        global model          
        # Set the model path
        model_path = Path("./text.model.bin")
        # Check to see if we have the model saved
        if not model_path.is_file():
            # Model is not saved, lets create it and save it
            sentences = word2vec.Text8Corpus('./text8')
            model = word2vec.Word2Vec(sentences, size=200)
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
        if word['operation'] == True:
            logging.info("Word: %s, Operation: Addition", word['content'].lower())
            adds.append(word['content'].lower())
        else:
            logging.info("Word: %s, Operation: Subtraction", word['content'].lower())
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
context = ('./myserver.crt', './myserver.key')


if not thread.isAlive():
    logging.info("Starting thread")
    thread = Word2VecModel()
    thread.start()


if __name__ == "__main__":
    context = ('./myserver.crt', './myserver.key')
    app.run(threading=True, ssl_context=context)