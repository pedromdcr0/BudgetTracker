from flask import Flask, render_template, request, flash, redirect, session, url_for

app = Flask(__name__)

app.secret_key = "peanut"

@app.route('/')
def index():
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True)