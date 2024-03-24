from flask import Flask, render_template, redirect, url_for

app = Flask("__main__")


@app.route("/")
def index():
    return redirect(url_for('cadastro'))

@app.route("/cadastro")
def cadastro():
    return render_template("index.html")
app.run()