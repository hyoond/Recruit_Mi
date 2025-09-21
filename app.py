from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'secretkey123'

@app.route("/")
def start():
    username = ""
    return render_template ("homepage.html")

@app.route('/homepage', methods=["POST"])
def homepage():
    username = request.form["username"]
    return render_template ("preferences.html")

if __name__ == '__main__':
    app.run(debug=True)