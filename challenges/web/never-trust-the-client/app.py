# /// script
# dependencies = [
#   "flask"
# ]
# ///
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    make_response,
)
import hashlib

app = Flask(__name__)
app.secret_key = "super_secret_cat_key"  # Change this in production!

ALLOWED_HASHES = [
    # "ilovecats"
    "81a103d766de77d8a2224fbab8294cc9e956c8224b30041c668cc98c205b8b82"
]


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if username != "admin" and password_hash in ALLOWED_HASHES:
                resp = make_response(redirect(url_for("index")))
                resp.set_cookie("username", username)
                return resp
            else:
                error = "Invalid password! Only true cat lovers allowed."
        else:
            error = "Please enter both username and password."

    username = request.cookies.get("username")
    return render_template("index.html", username=username, error=error)


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("username", "", expires=0)
    return resp


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
