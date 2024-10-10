from flask import Flask, render_template, redirect, url_for, request,jsonify
import os
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    # Change this URL to the YouTube video you want to redirect to

    return render_template('index.html')

@app.route('/execute', methods=['POST', 'GET'])
def execute():
    #get the command from the command line
    #command = request.form['command']
    command = "ls"

    try:
        # Execute the command
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Combine stdout and stderr
        output = result.stdout + result.stderr
        retval = result.returncode
    except Exception as e:
        output = str(e)
        retval = 1
    #return the result to the user
    return jsonify(result=output, retval=retval)



if __name__ == '__main__':
    app.run(debug=True)