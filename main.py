from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Token Checker</title>
    <style>
        body {
            background-color: #f2f2f2;
            font-family: Arial, sans-serif;
        }
        .container {
            width: 300px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .container h1 {
            text-align: center;
        }
        .container form {
            margin-top: 20px;
        }
        .container form input[type="text"] {
            width: 100%;
            height: 30px;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .container form button[type="submit"] {
            width: 100%;
            height: 30px;
            background-color: #4CAF50;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .container form button[type="submit"]:hover {
            background-color: #3e8e41;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Token Checker</h1>
        <form method="post">
            <input type="text" name="access_token" placeholder="Enter Facebook Access Token">
            <button type="submit">Check Token</button>
        </form>
        {% if result %}
            <div class="result">
                {{ result }}
            </div>
        {% endif %}
        {% if uid_link %}
            <div class="result">
                UID Link: <a href="{{ uid_link }}">{{ uid_link }}</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    uid_link = None
    if request.method == "POST":
        access_token = request.form.get("access_token")
        url = f"https://graph.facebook.com/me?access_token={access_token}"
        try:
            response = requests.get(url).json()
            if "id" in response:
                result = f"Valid Token - User: {response['name']} (ID: {response['id']})"
                uid_link = f"https://www.facebook.com/{response['id']}"
            else:
                result = "Invalid Token"
        except:
            result = "Error Checking Token"
    return render_template_string(html_template, result=result, uid_link=uid_link)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
