from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'secretkey123'

@app.route('/homepage', methods=["GET"])
def homepage():
    username = request.form["username"]
    return render_template("homepage.html", username=username)