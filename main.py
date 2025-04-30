from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """ 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title style="color: red;">Facebook Reaction Tool</title> 
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
    <h1>Facebook Reaction Tool</h1> 
    <div class="info"> 
        <p class="developer">SONU SISODIA JI</p> 
        <p class="contact">CONTACT: 7500170115</p> 
    </div> 
    <form method="POST"> 
        <textarea name="ids" placeholder="Enter Post IDs (separated by comma)"></textarea> 
        <select name="reaction_type"> 
            <option value="LIKE">Like</option> 
            <option value="LOVE">Love</option> 
            <option value="HAHA">Haha</option> 
            <option value="WOW">Wow</option> 
            <option value="SAD">Sad</option> 
            <option value="ANGRY">Angry</option> 
        </select> 
        <button type="submit">React</button> 
    </form> 
    {% if message %} 
        <p style="color: green">{{ message }}</p> 
    {% endif %} 
    {% if error %} 
        <p style="color: red">{{ error }}</p> 
    {% endif %} 
</body> 
</html> 
"""

def get_tokens():
    try:
        with open('tokens.txt', 'r') as f:
            tokens = f.read().splitlines()
        return tokens
    except Exception as e:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ids = request.form.get('ids').split(',')
        ids = [id.strip() for id in ids]
        reaction_type = request.form.get('reaction_type')
        
        if not ids:
            return render_template_string(HTML_TEMPLATE, error="IDs are required")
        
        tokens = get_tokens()
        if not tokens:
            return render_template_string(HTML_TEMPLATE, error="No tokens found")
        
        for post_id in ids:
            for token in tokens:
                url = f"https://graph.facebook.com/v18.0/{post_id}/reactions"
                params = {
                    "access_token": token,
                    "type": reaction_type
                }
                try:
                    response = requests.post(url, params=params)
                    if response.status_code == 200:
                        print(f"Reaction posted on {post_id} with token {token}")
                    else:
                        print(f"Error posting reaction on {post_id} with token {token}: {response.text}")
                except Exception as e:
                    print(f"Error posting reaction on {post_id} with token {token}:
