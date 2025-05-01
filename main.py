from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """ 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Facebook Reaction Tool</title> 
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
            border: 2px solid #87CEEB; 
            padding: 20px; 
            width: 400px; 
            margin: 20px auto; 
            border-radius: 10px; 
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); 
            background-color: #f2f2f2; 
        } 
        .developer { 
            color: #00ff00; 
            text-decoration: underline; 
        } 
        .contact { 
            color: #0000ff; 
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
        <p class="developer">SONU</p> 
        <p class="contact">CONTACT: 7351774544</p> 
    </div> 
    <form method="POST"> 
        <input type="text" name="access_token" placeholder="Enter Access Token" required><br><br>
        <input type="text" name="post_id" placeholder="Enter Post ID" required><br><br>
        <select name="reaction_type"> 
            <option value="LIKE">Like</option> 
            <option value="LOVE">Love</option> 
            <option value="HAHA">Haha</option> 
            <option value="WOW">Wow</option> 
            <option value="SAD">Sad</option> 
            <option value="ANGRY">Angry</option> 
        </select><br><br> 
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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        post_id = request.form.get('post_id')
        reaction_type = request.form.get('reaction_type')
        
        if not access_token or not post_id or not reaction_type:
            return render_template_string(HTML_TEMPLATE, error="All fields are required")

        url = f"https://graph.facebook.com/v18.0/{post_id}/reactions"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        data = {
            "type": reaction_type
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            json_response = response.json()
            if response.status_code == 200 and json_response.get("success", True):
                return render_template_string(HTML_TEMPLATE, message="Reaction posted successfully")
            else:
                error_msg = json_response.get("error", {}).get("message", "Unknown error")
                return render_template_string(HTML_TEMPLATE, error=f"Error: {error_msg}")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=f"Exception: {str(e)}")

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
