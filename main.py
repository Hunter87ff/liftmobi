from flask import Flask, render_template, jsonify, redirect, request, url_for
import json, logging
import ast
import sqlite3

app = Flask(__name__)
app.static_folder = "static"

def get_(data):
	x = sqlite3.connect("data.db")
	conn = x.cursor()
	y = conn.execute(f"SELECT  * FROM msgs WHERE name='{data['name']}' AND subject='{data['subject']}'")
	return y.fetchall()

def get_all_db():
	x = sqlite3.connect("data.db").cursor().execute(f"SELECT  * FROM msgs")
	data = x.fetchall()
	return data

def load():
	x = open("data.txt", 'r')
	d = int(x.read())
	c = d + 1
	open("data.txt", "w").write(str(c))
	return(c-1)


users = {
	"hunter@hunter.io": "hunterop87",
	"jazk@gmail.com": "myway99",
	"propaco@gmail.com" : "liftmobi12"
}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/portal")
def dash():
	messages = get_all_db()
	obj = {
	"view" : open("data.txt", 'r').read(),
	"lmsg" : len(messages),
	"lmem": len(users),
	"uptime" : "4h 32m",
	"messages" : messages,
	"members" : users
	}
	return render_template("dashboard.html", obj=obj)


@app.route("/api/portal")
def api_portal():
	messages = get_all_db()
	obj = {
	"view" : open("data.txt", 'r').read(),
	"lmsg" : len(messages),
	"lmem": len(users),
	"uptime" : "4h 32m",
	"messages" : messages,
	"members" : users
	}
	return jsonify(obj)


@app.route("/api/contact", methods=["POST"])
def  api_contact():
	data = request.form.to_dict()
	name = data["name"].replace('"', "'")
	email = data["email"].replace('"', "'")
	subject = data["subject"].replace('"', "'")
	desc = data["desc"].replace('"', "'")
	x = sqlite3.connect("data.db")
	y = x.cursor()
	y.execute(f"""INSERT INTO msgs VALUES("{name}", "{email}", "{subject}", "{desc}")""")
	x.commit()
	return "success", 200

@app.route("/api/oauth", methods=["POST"])
def api_oauth():
	try:
		data = request.form.to_dict()
		print(data)

		if users[data['email']] == data["pass"]:
			return "success", 200
		else:
			return "Invalid email/password", 200
	except KeyError as e:
		return f"Invalid {e}"

@app.route("/api/load", methods=["POST"])
def api_load():
	ls = load()
	return f"{ls}", 200

@app.route("/api/delmsg", methods=["POST"])
def api_delmsg():
	data = request.form.to_dict()
	print(data)
	if get_(data) != None:
		x = sqlite3.connect("data.db")
		conn = x.cursor()
		conn.execute(f"DELETE FROM msgs WHERE name='{data['name']}' AND email='{data['email']}' AND subject='{data['subject']}'")
		x.commit()
		return redirect("/portal"), 200
	else:
		return "Something Went Wrong. failed to delete!!", 200

app.run(host="0.0.0.0", port=8080)
