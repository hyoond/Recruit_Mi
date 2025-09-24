from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secretkey123'

if not os.path.exists("database.db"):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS preferences(
                   type TEXT)
                   ''')
    cursor.execute(' INSERT OR IGNORE INTO preferences(type) VALUES ("Sports"),("Art"),("Gaming"),("Reading"),("Desgin"),("Music")')
    conn.commit()
    conn.close()


@app.route("/")
def start():
    return render_template("homepage.html")

@app.route('/homepage', methods=["POST"])
def homepage():
    global username
    global contact_num
    username = request.form["username"]
    contact_num = request.form["contact_num"]
    return redirect(url_for('preferences'))

@app.route('/preferences', methods=["GET","POST"])
def preferences():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM preferences')
    preferences = cursor.fetchall()
    if request.method == "POST":
        global selected
        selected = request.form.getlist("preferences")
        cursor.execute ('''CREATE TABLE IF NOT EXISTS user(
                        username TEXT,
                        contact_num TEXT,
                        preferences TEXT)
                        ''')
        cursor.execute (''' INSERT INTO user(username, contact_num, preferences)
                       VALUES (?,?,?)''',(username,contact_num,selected) )
        cursor.commit()

        return redirect(url_for("interested"))
    
    return render_template ("preferences.html", preferences = preferences, username = username)

@app.route('/interested', methods=["GET","POST"])
def interested():
    cursor.execute ('''SELECT * FROM user
                    WHERE preferences = ? 
                    ''', (selected))
    return render_template(interested.html)

if __name__ == '__main__':
    app.run(debug=True)