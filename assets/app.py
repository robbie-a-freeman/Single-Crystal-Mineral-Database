from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Python Flask!"

@app.route("/submit")
def submit():
    input = request.form['mineral_class'];
    return input

if __name__ == "__main__":
    app.run()
