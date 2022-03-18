from flask import Flask, render_template, redirect, abort, url_for, make_response
from flask import request
import subprocess
import time
import random

app = Flask(__name__)

@app.route("/")
def index():
    r = make_response(render_template("index.html"))

    return r

@app.route("/check", methods=["POST"])
def check():
    fail_proba = 10

    if random.choices([True, False], weights=(fail_proba, 100 - fail_proba))[0]:
        choice = random.choices(['abort', 'redirect', 'sleep', 'redirect_inf', 'exception'])[0]
        if choice == "abort":
            return abort(403)
        elif choice == "redirect":
            return redirect("http://somethingwentwrong")
        elif choice == "sleep":
            time.sleep(60 * 2)
        elif choice == "redirect_inf":
            return redirect(url_for("redirect_inf"))
        elif choice == "exception":
            raise Exception()

    ip = request.form["check_alive"]

    command = f"ping -c1 {ip}"
    result = subprocess.check_output(command, shell=True).decode("UTF-8").split("\n")
    r = make_response(render_template("index.html", result=result))

    return r

@app.route("/redirect_inf")
def redirect_inf():
    return redirect(url_for("redirect_inf"))

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
