#Import essential modules
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

#Crucial Code to build flask enviroment
app = Flask(__name__)
app.secret_key = 'secretkey123'

#Detect whether the database file is exist or not and then insert basic interests
if not os.path.exists("database.db"):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS preferences(
                   type TEXT NOT NULL)
                   ''')
    cursor.execute(' INSERT OR IGNORE INTO preferences(type) VALUES ("Sports"),("Art"),("Gaming"),("Reading"),("Desgin"),("Music")')
    conn.commit()
    conn.close()

#Whole system start with this function and then will direct to the homepage
@app.route("/")
def start():
    return render_template("homepage.html")

#homepage function to render the homepage.html and receive the variable username and contact number then pass to preferences function
@app.route('/homepage', methods=["POST"])
def homepage():
    session['username'] = request.form["username"]
    session['contact_num'] = request.form["contact_num"]
    return redirect(url_for('preferences'))

#Preferences function to render preference html page while also create and insert user info received from user input in homepage, also retrive interests then pass to preferences page to display the interests selection
@app.route('/preferences', methods=["GET", "POST"])
def preferences():
    if request.method == "POST":
        username = session.get("username", "")
        contact_num = session.get("contact_num", "")
        selected = request.form.getlist("preferences")
        selected_str = ",".join(selected)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                        username TEXT,
                        contact_num TEXT,
                        preferences STRING (255))''')
        cursor.execute('''INSERT INTO user(username, contact_num, preferences)
                          VALUES (?, ?, ?)''', (username, contact_num, selected_str))
        conn.commit()
        conn.close()

        return redirect(url_for('interested', selected_str=selected_str, username=username))

    username = request.args.get('username', '')
    contact_num = request.args.get('contact_num', '')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM preferences')
    preferences = cursor.fetchall()
    conn.close()

    return render_template("preferences.html", preferences=preferences, username=username, contact_num=contact_num)


#Interested function to render interested html page and also received user's preferences and then search in the database in order to show the people with the same interests
@app.route('/interested', methods=["GET","POST"])
def interested():
    selected_str = request.args.get('selected_str', '')
    username = session.get("username", '')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM user
                      WHERE preferences LIKE ?
                      EXCEPT 
                      SELECT * FROM user
                      WHERE username = ? ''', (f"%{selected_str}%",username))
    people = cursor.fetchall()
    return render_template("interested.html", people=people)

#Custom function to render custom html page and to receive input from user on their custom interest then inserts into the preferences table
@app.route('/custom', methods=["POST","GET"])
def custom():
    custom_interest = request.form.get("custom_interest", "")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO preferences(type) VALUES(?)', (custom_interest,))
    conn.commit()
    if request.method == "POST":
        return redirect(url_for("preferences"))
    return render_template("custom.html", custom_interest = custom_interest)

#Crucial ending code for flask
if __name__ == '__main__':
    app.run(debug=True)

    