from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
GRAPH_API_URL = "https://graph.facebook.com/v18.0"

# Updated HTML & CSS Template
HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Token Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: url('https://i.ibb.co/qYtGC5Kz/In-Shot-20250306-044013972.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 90%;
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.3);
        }
        h2 {
            margin-bottom: 20px;
            font-size: 22px;
            text-transform: uppercase;
        }
        input {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            background: black;
            color: white;
            border-radius: 5px;
            text-align: center;
        }
        button {
            width: 95%;
            padding: 10px;
            background: blue;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: darkblue;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background: black;
            border-radius: 5px;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Page Token Extractor</h2>
        <form method="POST">
            <input type="text" name="token" placeholder="Enter Access Token" required>
            <button type="submit">Extract Token</button>
        </form>
        {% if pages %}
        <div class="result">
            <h3>Page Tokens:</h3>
            <ul>
                {% for page in pages %}
                <li><strong>{{ page.name }}</strong> - Page ID: {{ page.id }} - Page Token: {{ page.token }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        {% if groups %}
        <div class="result">
            <h3>Messenger Groups:</h3>
            <ul>
                {% for group in groups %}
                <li><strong>{{ group.name }}</strong> - UID: {{ group.id }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        {% if error %}
        <p class="result" style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        access_token = request.form.get('token')
        if not access_token:
            return render_template_string(HTML_TEMPLATE, error="Token is required")
        
        # Get page tokens
        url_pages = f"{GRAPH_API_URL}/me/accounts?fields=id,name,access_token&access_token={access_token}"
        try:
            response_pages = requests.get(url_pages)
            data_pages = response_pages.json()
            pages = []
            if "data" in data_pages:
                for page in data_pages["data"]:
                    pages.append({
                        "id": page["id"],
                        "name": page["name"],
                        "token": page["access_token"]
                    })
            else:
                return render_template_string(HTML_TEMPLATE, error="Invalid token or no pages found")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error="Something went wrong")

        # Get messenger groups
        url_groups = f"{GRAPH_API_URL}/me/conversations?fields=id
