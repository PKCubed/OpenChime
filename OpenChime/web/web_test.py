from flask import Flask, request, render_template
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) # Modifies the behavior of the index function.
def index():
	if request.method == 'POST':
		if request.form['submit_button'] == 'Manual Bell':
			print("manual bell")
		elif request.form['submit_button'] == 'Test Chime':
			print("test chime")
		else:
			print("unknown button")
	return render_template("index.html", web_time = "2:43")

@app.route("/info")
def info():
	return "<p>The web user interfase is not currently availible.<p>"

if __name__ == "__main__":
	app.run(host="0.0.0.0")