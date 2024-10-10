from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)

username = "kidz";
password = "l3t_kidz_1n_th4nk_you_machine#1!"

@app.route('/')
def index():
    # Change this URL to the YouTube video you want to redirect to

    return render_template('index.html', username=username, password=password)

@app.route('/auth', methods=["POST"])
def auth():
    if username == request.form['username'] and password == request.form['password']:
        image_folder = 'static/images'
        # List all image files in the directory
        images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        return render_template("hackTheNasaOperation.html", images = images)
    #rick roll
    # Change this URL to the YouTube video you want to redirect to
    youtube_url = 'https://www.youtube.com/watch?v=xbxQxK6gFnI'
    return render_template('countdown.html', youtube_url=youtube_url)


if __name__ == '__main__':
    app.run(debug=True)