from flask import Flask
from flask import request
from flask import render_template
import os
from datetime import datetime
import sqlite3
import json
import urllib.parse

# ======= CONFIGURATION =======
DB_NAME = "mineftp_reg.db"
FILEBASE = ".\\filebase\\"
# =============================

init_connection = sqlite3.connect(DB_NAME)
init_cursor = init_connection.cursor()

init_cursor.execute('''
	CREATE TABLE IF NOT EXISTS users (
		username TEXT NOT NULL,
		password TEXT NOT NULL
	);
''')

init_cursor.execute('''
	CREATE TABLE IF NOT EXISTS uploads (
		username TEXT NOT NULL,
		filename TEXT NOT NULL,
		upload_date TEXT NOT NULL
	);
''')

init_connection.commit()
init_connection.close()

def dir_to_string(path):
	filestring = ""

	for v in os.listdir(path):
		filestring += v + "\n"

	print(filestring)
	return filestring

def db_execute(request):
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()

	cursor.execute(request)

	connection.commit()
	connection.close()

def db_getlist(tablename):
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()

	cursor.execute(f"SELECT * FROM {tablename}")
	list = cursor.fetchall()

	connection.close()
	return list

app = Flask(__name__, template_folder=".")

@app.route("/")
def test_conhadle():
	uploads = db_getlist("uploads")
	return render_template("index.html", uploads=uploads)

@app.route("/signup", methods=["post"])
def add_user():
	username = request.form.get("username")
	password = request.form.get("password")

	db_execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');")

	return "User registered!"

@app.route("/ftp", methods=["get", "post"])
def ftp_handle():
	if request.method == "POST":
		user = request.form.get("user")
		filename = request.form.get("filename")
		content = request.form.get("content")
		upload_date = str(datetime.now())

		print(f"Processing uploading request of {filename} by {user}...")

		#content = urllib.parse.unquote(content)
		content = content.replace("\r\n", "\n")
		content = content.rstrip("\n")

		with open(FILEBASE + filename, "w", encoding="ascii") as file:
			print(content, file=file)

		db_execute(f"INSERT INTO uploads (username, filename, upload_date) VALUES ('{user}', '{filename}', '{upload_date}');")
		return "File uploaded!"

	if request.method == "GET":
		filename = request.args.get("path")

		if filename == "ls":
			response = dir_to_string(FILEBASE)
			return response

		content = ""
		try:
			with open(FILEBASE + filename, "r") as file:
				content = file.read()

			return content

		except FileNotFoundError:
			return f"File {filename} not found on the server!"

	return "Idi nahui"

@app.route("/coordination", methods=["post"])
def coord_handle():
	channel_name = request.form.get("channelName")
	coord_x = request.form.get("coordX")
	coord_y = request.form.get("coordY")
	coord_z = request.form.get("coordZ")
	message = request.form.get("message")

	print(channel_name)
	return "pidor is " + channel_name

if __name__ == "__main__":
	print("Starting app!")
	app.run(debug=True, host="0.0.0.0", port=5000)