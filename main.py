from flask import Flask, request, render_template_string, redirect, url_for

import os

import time

import requests

import sys

app = Flask(__name__)

# New Logo

logo = """

<h1 style="color: blue; text-align: center;">

    CREATOR => SONU SISODIA JI<br>

    ALONE => BADMASH<br>

    FACEBOOK => <br>

    WHATSAPP => 7500170115

</h1>

"""

# CSS for pink background and blue text

css = """

<style>

    body {

        background-color: pink;

        color: blue;

        font-family: Arial, sans-serif;

    }

    .container {

        width: 50%;

        margin: auto;

        text-align: center;

    }

    .button {

        background-color: blue;

        color: white;

        padding: 10px 20px;

        border: none;

        cursor: pointer;

    }

    .button:hover {

        background-color: darkblue;

    }

    .upload-label {

        display: block;

        margin: 10px 0;

    }

    .select-option {

        margin: 20px 0;

    }

    .select-option a {

        color: blue;

        text-decoration: none;

        font-size: 18px;

    }

    .select-option a:hover {

        text-decoration: underline;

    }

</style>

"""

# Home Page with Login Form

@app.route('/')

def index():

    return render_template_string(f'''

        {css}

        <div class="container">

            {logo}

            <form action="/login" method="post">

                <label for="username" style="display: block; margin: 10px 0;">Username:</label>

                <input type="text" id="username" name="username" style="padding: 5px;">

                <label for="password" style="display: block; margin: 10px 0;">Password:</label>

                <input type="password" id="password" name="password" style="padding: 5px;">

                <button type="submit" class="button">Login</button>

            </form>

        </div>

    ''')

# Login Route

@app.route('/login', methods=['POST'])

def login():

    username = request.form['username']

    password = request.form['password']

    if username == 'Legend' and password == 'Devil':

        return redirect(url_for('dashboard'))

    else:

        return "Incorrect Password", 401

# Dashboard with Selectable Options

@app.route('/dashboard')

def dashboard():

    return render_template_string(f'''

        {css}

        <div class="container">

            {logo}

            <div class="select-option">

                <a href="/send_messages">Convo / IB Tool</a>

            </div>

            <div class="select-option">

                <a href="/comment_send">Post Tool</a>

            </div>

            <div class="select-option">

                <a href="/owner">Owner Facebook ID</a>

            </div>

        </div>

    ''')

# Send Messages Route

@app.route('/send_messages', methods=['GET', 'POST'])

def send_messages():

    if request.method == 'POST':

        name = request.form['name']

        tokken_file = request.files['tokken']

        convo_id = request.form['convo_id']

        gali_file = request.files['gali']

        haters_name = request.form['haters_name']

        timm = int(request.form['timm'])

        # Save uploaded files

        tokken_path = os.path.join('uploads', tokken_file.filename)

        gali_path = os.path.join('uploads', gali_file.filename)

        tokken_file.save(tokken_path)

        gali_file.save(gali_path)

        try:

            with open(tokken_path, 'r') as file:

                tokens = file.readlines()

            with open(gali_path, 'r') as file:

                messages = file.readlines()

        except FileNotFoundError:

            return "File Not Found", 404

        access_tokens = [token.strip() for token in tokens]

        num_messages = len(messages)

        max_tokens = min(len(tokens), num_messages)

        headers = {

            'Connection': 'keep-alive',

            'Cache-Control': 'max-age=0',

            'Upgrade-Insecure-Requests': '1',

            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',

            'Accept-Encoding': 'gzip, deflate',

            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',

            'referer': 'www.google.com'

        }

        results = []

        for message_index in range(num_messages):

            token_index = message_index % max_tokens

            access_token = access_tokens[token_index]

            message = messages[message_index].strip()

            url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"

            parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}

            response = requests.post(url, json=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

            if response.ok:

                results.append(f"Message {message_index + 1} sent successfully at {current_time}")

            else:

                results.append(f"Failed to send message {message_index + 1} at {current_time}")

            time.sleep(timm)

        return "<br>".join(results)

    return render_template_string(f'''

        {css}

        <div class="container">

            {logo}

            <h2>Send Messages</h2>

            <form method="post" enctype="multipart/form-data">

                <label for="name" class="upload-label">Your Name:</label>

                <input type="text" id="name" name="name" required><br>

                <label for="tokken" class="upload-label">Upload Token File:</label>

                <input type="file" id="tokken" name="tokken" required><br>

                <label for="convo_id" class="upload-label">Conversation ID:</label>

                <input type="text" id="convo_id" name="convo_id" required><br>

                <label for="gali" class="upload-label">Upload Abuse File:</label>

                <input type="file" id="gali" name="gali" required><br>

                <label for="haters_name" class="upload-label">Haters Name:</label>

                <input type="text" id="haters_name" name="haters_name" required><br>

                <label for="timm" class="upload-label">Speed in Seconds:</label>

                <input type="number" id="timm" name="timm" required><br>

                <button type="submit" class="button">Send</button>

            </form>

        </div>

    ''')

# Comment Send Route

@app.route('/comment_send', methods=['GET', 'POST'])

def comment_send():

    if request.method == 'POST':

        name = request.form['name']

        tokken_file = request.files['tokken']

        profile_id = request.form['profile_id']

        convo_id = request.form['convo_id']

        gali_file = request.files['gali']

        haters_name = request.form['haters_name']

        timm = int(request.form['timm'])

        # Save uploaded files

        tokken_path = os.path.join('uploads', tokken_file.filename)

        gali_path = os.path.join('uploads', gali_file.filename)

        tokken_file.save(tokken_path)

        gali_file.save(gali_path)

        try:

            with open(tokken_path, 'r') as file:

                tokens = file.readlines()

            with open(gali_path, 'r') as file:

                messages = file.readlines()

        except FileNotFoundError:

            return "File Not Found", 404

        access_tokens = [token.strip() for token in tokens]

        num_messages = len(messages)

        max_tokens = min(len(tokens), num_messages)

        headers = {

            'Connection': 'keep-alive',

            'Cache-Control': 'max-age=0',

            'Upgrade-Insecure-Requests': '1',

            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',

            'Accept-Encoding': 'gzip, deflate',

            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',

            'referer': 'www.google.com'

        }

        results = []

        for message_index in range(num_messages):

            token_index = message_index % max_tokens

            access_token = access_tokens[token_index]

            message = messages[message_index].strip()

            url = f'https://graph.facebook.com/v15.0/{profile_id}_{convo_id}/comments'

            parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}

            response = requests.post(url, json=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

            if response.ok:

                results.append(f"Comment {message_index + 1} sent successfully at {current_time}")

            else:

                results.append(f"Failed to send comment {message_index + 1} at {current_time}")

            time.sleep(timm)

        return "<br>".join(results)

    return render_template_string(f'''

        {css}

        <div class="container">

            {logo}

            <h2>Comment Send</h2>

            <form method="post" enctype="multipart/form-data">

                <label for="name" class="upload-label">Your Name:</label>

                <input type="text" id="name" name="name" required><br>

                <label for="tokken" class="upload-label">Upload Token File:</label>

                <input type="file" id="tokken" name="tokken" required><br>

                <label for="profile_id" class="upload-label">Profile ID:</label>

                <input type="text" id="profile_id" name="profile_id" required><br>

                <label for="convo_id" class="upload-label">Conversation ID:</label>

                <input type="text" id="convo_id" name="convo_id" required><br>

                <label for="gali" class="upload-label">Upload Abuse File:</label>

                <input type="file" id="gali" name="gali" required><br>

                <label for="haters_name" class="upload-label">Haters Name:</label>

                <input type="text" id="haters_name" name="haters_name" required><br>

                <label for="timm" class="upload-label">Delay:</label>

                <input type="number" id="timm" name="timm" required><br>

                <button type="submit" class="button">Send</button>

            </form>

        </div>

    ''')

# Owner Route

@app.route('/owner')

def owner():

    os.system("xdg-open https://www.facebook.com/GOD.OFF.SERVER")

    return "Owner page opened in browser."

# Create uploads directory if it doesn't exist

if not os.path.exists('uploads'):

    os.makedirs('uploads')

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=20661, debug=True)
