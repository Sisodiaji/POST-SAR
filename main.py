from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title style="color: red;">Conversation Script</title>
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
  <h1>Conversation Script</h1>
  <div class="info">
    <p class="developer">SONU SISODIA JI</p>
    <p class="contact">CONTACT: 7500170115</p>
  </div>
  <form method="POST">
    <input type="text" name="message" placeholder="Enter your message">
    <button type="submit">Send</button>
  </form>
  {% if response %}
    <h2>Response:</h2>
    <p>{{ response }}</p>
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
        message = request.form.get('message')
        if not message:
            return render_template_string(HTML_TEMPLATE, error="Message is required")

        # Process the message and generate a response
        response = process_message(message)
        return render_template_string(HTML_TEMPLATE, response=response)
    return render_template_string(HTML_TEMPLATE)

def process_message(message):
    # This function can be used to process the message and generate a response
    # For example, you can use a machine learning model or a simple rule-based system
    return "Thank you for your message: " + message

if __name__ == '__main__':
    app.run(debug=True)
