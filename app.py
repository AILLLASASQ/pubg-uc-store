import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

API_URL = "https://api.game4station.com/api/checkNameEl"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Origin": "https://game4station.com",
    "Referer": "https://game4station.com/",
}

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/player", methods=["GET"])
def get_player():
    player_id = request.args.get("id", "").strip()
    if not player_id:
        return jsonify({"error": "أدخل الـ Player ID"}), 400
    if not player_id.isdigit():
        return jsonify({"error": "الـ ID يجب أن يكون أرقاماً فقط"}), 400

    payload = {"game": "pubgm", "userId": player_id, "serverId": None}
    try:
        res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        try:
            data = res.json()
        except ValueError:
            return jsonify({
                "error": "الرد ليس JSON",
                "debug_status": res.status_code,
                "debug_body": res.text[:500]
            }), 502

        if data.get("status") == "OK":
            info = data.get("data", {})
            if info.get("valid") == "valid":
                return jsonify({"name": info.get("name", "غير معروف"), "id": player_id})
            return jsonify({"error": "اللاعب غير موجود — تأكد من الـ ID"}), 404
        return jsonify({"error": "لم يتم العثور على اللاعب", "debug": data}), 404

    except requests.exceptions.Timeout:
        return jsonify({"error": "انتهت مهلة الاتصال"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "فشل الاتصال بالخادم"}), 502
    except Exception as e:
        return jsonify({"error": f"خطأ: {str(e)}"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)