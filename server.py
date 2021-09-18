from flask import Flask, render_template, redirect, request, url_for, flash, session
import os
import pyotp

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
  form_user = request.form.get("username")
  form_pass = request.form.get("password")
  if request.method == 'POST':
    if form_user == app.config["USER"] and form_pass == app.config["PASS"]:
      session['username'] = form_user
      #does the user have 2FA enabled? Let's assume so...
      return redirect(url_for("OTP_auth"))
    else:
      flash("Invalid credentials. Please try again.")
  return redirect(url_for("index"))

@app.route("/login/auth", methods=['GET', 'POST'])
def OTP_auth():
  if session['username'] == None:
    return redirect(url_for('login'))
  if request.method == 'POST':
    #verify OTP
    totp_instance = pyotp.TOTP(app.config["OTP_CODE"])
    valid = totp_instance.verify(request.form.get("otp"))
    if valid:
      return render_template("success.html")
    else:
      flash("Invalid code. Please try again.")
  else:
    if app.config["OTP_ENABLED"] == "True":
      return render_template('auth.html')
    else:
      app.config["OTP_ENABLED"] = "True"
      return render_template('auth.html', secret_key=app.config["OTP_CODE"])
  return redirect(url_for("OTP_auth"))


if __name__ == "__main__":
  app.config["USER"] = "username"
  app.config["PASS"] = "password"
  app.config["OTP_CODE"] = pyotp.random_base32()
  app.config["OTP_ENABLED"] = "False"
  app.config["SECRET_KEY"] = os.urandom(16).hex()
  app.run(debug=True)