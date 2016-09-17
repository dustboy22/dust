from flask import Flask, request, redirect, render_template, url_for, session

import os
import webpage

app = Flask(__name__)
app.secret_key = os.urandom(24)

webmaster = webpage.WebMaster()


@app.route("/")
def frontpage():
	webmaster.prune_posts()

	return render_template("frontpage.html", webmaster = webmaster)


@app.route("/help")
def help():
	return render_template("help.html", webmaster = webmaster)


@app.route("/new", methods = ["POST", "GET"])
def new_post():
	if request.method == "POST":
		if not request.form["content"]:
			return render_template("message.html", message = "error: no content", webmaster = webmaster)

		if request.form["captcha"] != session["cap"]:
			return render_template("message.html", message = "failed captcha", webmaster = webmaster)

		title = request.form["content"].split("\n")[0]
		content = "".join(request.form["content"].split("\n")[1:])

		webmaster.new_post(title, content)

		return redirect(url_for("frontpage"))

	else:
		cap = webpage.Captcha()
		session["cap"] = cap.code
		return render_template("new.html", webmaster = webmaster, captcha = cap)


@app.route("/post/<int:post_id>", methods = ["POST", "GET"])
def view_post(post_id):
	if request.method == "POST":
		post = webmaster.get_post(post_id)

		if not post:
			return render_template("message.html", message = "post not found", webmaster = webmaster)

		if not request.form["comment"]:
			return render_template("message.html", message = "error: no content", webmaster = webmaster)

		if request.form["captcha"] != session["c_cap"]:
			return render_template("message.html", message = "failed captcha", webmaster = webmaster)
			
		post.new_comment(request.form["comment"])
	
		return redirect(url_for("view_post", post_id=post.post_id))

	else:
		post = webmaster.get_post(post_id)
	
		if not post:
			return render_template("message.html", message = "post not found", webmaster = webmaster)

		cap = webpage.Captcha()
		session["c_cap"] = cap.code

		return render_template("post.html", post = post, webmaster = webmaster, captcha = cap)


if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0')