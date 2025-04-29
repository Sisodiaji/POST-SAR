from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title style="color: red;">Page Token Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-image: url('https://i.ibb.co/r2LjfV3x/2d8b98aa48e24c185694c9f04989eed8.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .info {
            border: 2px solid #87CEEB; /* Aasmani color */
            padding: 20px;
            width: 400px;
            margin: 20px auto;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            background-color: #f2f2f2;
        }
        .developer {
            color: #00ff00; /* Green color */
            text-decoration: underline;
        }
        .contact {
            color: #0000ff; /* Blue color */
        }
        h1 {
            color: red;
        }
        button {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Page Token Extractor</h1>
    <div class="info">
        <p class="developer">𝗦𝗢𝗡𝗨 𝗦𝗜𝗦𝗢𝗗𝗜𝗔 𝗝𝗜</p>
        <p class="contact">𝗖𝗢𝗡𝗧𝗔𝗖𝗧: 7500170115</p>
    </div>
    <form method="POST">
        <input type="text" name="token" placeholder="Enter Access Token">
        <button type="submit">Submit Token</button>
    </form>
    {% if pages %}
    <h2>Page Tokens:</h2>
    <ul>
        {% for page in pages %}
        <li>Page ID: {{ page.page_id }} - Page Name: {{ page.page_name }} - Page Token: {{ page.page_token }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    {% if error %}
    <p style="color: red">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        access_token = request.form.get('token')
        if not access_token:
            return render_template_string(HTML_TEMPLATE, error="Token is required")
        
        url = f"https://graph.facebook.com/v18.0/me/accounts?fields=id,name,access_token&access_token={access_token}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return render_template_string(HTML_TEMPLATE, error="Invalid token or API error")
            
            data = response.json()
            if "data" in data:
                pages = []
                for page in data["data"]:
                    pages.append({
                        "page_id": page["id"],
                        "page_name": page["name"],
                        "page_token": page["access_token"]
                    })
                return render_template_string(HTML_TEMPLATE, pages=pages)
            else:
                return render_template_string(HTML_TEMPLATE, error="Invalid token or no pages found")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error="Something went wrong")
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
