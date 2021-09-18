from flask import Flask, render_template, redirect, request, url_for, flash, session

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
  message = None
  form_user = request.form.get("username")
  form_pass = request.form.get("password")
  if request.method == 'POST':
    if form_user == app.config["USER"] and form_pass == app.config["PASS"]:
      return render_template('success.html')
    else:
      flash("Invalid credentials. Please try again.")
  return redirect(url_for("index"))


if __name__ == "__main__":
  app.config["USER"] = "username"
  app.config["PASS"] = "password"
  app.config["SECRET_KEY"] = b'!abexc/)#0021&'
  app.run(debug=True)