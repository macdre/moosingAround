# Web App for MCDA5570-Assignment02
# By: macdre

from flask import Flask import render_template
app = Flask(__name__)

@app.route('/')
	def index(): return render_template('index.html')

@app.route("/hello")
def hello():
    return "Hello there! Just moosing around"

if __name__ == "__main__":
    app.run()

