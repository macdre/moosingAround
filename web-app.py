# Web App for MCDA5570-Assignment02
# By: macdre

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Not much going on here, try /hello for more excitement."

@app.route("/hello")
def hello():
    return "Hello MCDA5570!"

if __name__ == "__main__":
    app.run()

