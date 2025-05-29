from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SONU TOKEN CHECKER</title>
    <style>
        /* CSS for styling elements */
        .error {
            color: red;
            font-weight: italic;
        }
        h1{
            text-align: center;
            border: double 2px white;
            font-family: cursive;
            font-size: 25px;
        }
        .btn, input, textarea {
            width: 100%;
            margin-top: 20px;
            background-color: blue;
            border: double 2px white;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            box-sizing: border-box;
        }
        input, textarea {
            outline: green;
            border: double 2px white;
            padding: 10px;
            background-color: black;
            color: white;
        }
        h2{
            text-align: center;
            font-size: 15px;
            border-radius: 20px;
            color: white;
            background-color: black;
            border: double 2px white;
        }
        label{
            color: white;
        }
        body{
            background-image: url('https://i.ibb.co/35rT2pRT/8ecc60c1daa4d03d8a734980cfd7ee7e.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
            background-attachment: fixed;
            color: white;
            height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            max-width: 350px;
            width: 100%;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
            box-shadow: 0 0 15px white;
            border: double 2px white;
            resize: none;
            background: rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>FACEBOOK TOKEN CHECKER</h1>
        <form method="post">
            <textarea name="access_tokens" placeholder="ENTER TOKENS (ONE TOKEN PER LINE)" required style="height: 150px;"></textarea>
            <button class="btn" type="submit">CHECK TOKENS</button>
        </form>
        {% if results %}
            <h2>Valid Tokens:</h2>
            {% for result in results['valid'] %}
                <h2 style="color: green;">{{ result }}</h2>
            {% endfor %}
            <h2>Invalid Tokens:</h2>
            {% for result in results['invalid'] %}
                <h2 style="color: red;">{{ result }}</h2>
            {% endfor %}
        {% endif %}
        <footer>
            <h2>THE LEGEND BOY SONU HERE</h2>
        </footer>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        access_tokens = request.form.get("access_tokens").splitlines()
        valid_tokens = []
        invalid_tokens = []
        for access_token in access_tokens:
            access_token = access_token.strip()
            if access_token:
                url = f"https://graph.facebook.com/me?access_token={access_token}"
                try:
                    response = requests.get(url).json()
                    if "id" in response:
                        valid_tokens.append(f"Token: {access_token} - User: {response['name']} (ID: {response['id']})")
                    else:
                        invalid_tokens.append(f"Invalid Token - {access_token}")
                except Exception as e:
                    invalid_tokens.append(f"Error checking token - {access_token}")
        results = {'valid': valid_tokens, 'invalid': invalid_tokens}
    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(debug
