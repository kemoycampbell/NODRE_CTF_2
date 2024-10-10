from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    # Change this URL to the YouTube video you want to redirect to

    return render_template('index.html')

@app.route('/reveal')
def reveal():
    return render_template("hackTheNasaOperationreveal.html")



if __name__ == '__main__':
    app.run(debug=True)