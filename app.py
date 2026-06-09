import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

MIDASBUY_URL = "https://www.midasbuy.com/midasbuy/ot/query/user"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Referer":    "https://www.midasbuy.com/midasbuy/us/buy/pubgm",
    "Accept":     "application/json, text/plain, */*",
    "Origin":     "https://www.midasbuy.com",
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

    params = {"game": "PUBGM", "uid": player_id, "checkNum": ""}
    try:
        res  = requests.get(MIDASBUY_URL, params=params, headers=HEADERS, timeout=10)
        data = res.json()
        ret_code = data.get("retCode", -1)
        if ret_code == 0:
            info = data.get("data", {})
            name = info.get("username") or info.get("name") or info.get("nickName", "")
            if not name:
                return jsonify({"error": "لم يتم العثور على الاسم"}), 404
            return jsonify({"name": name, "id": player_id})
        elif ret_code in [10006, 10001]:
            return jsonify({"error": "اللاعب غير موجود — تأكد من الـ ID"}), 404
        else:
            return jsonify({"error": f"خطأ من Midasbuy: {ret_code}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)