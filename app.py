import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

# ── تحميل API Key من متغيرات البيئة ──
PUBG_API_KEY = os.environ.get("PUBG_API_KEY", "")

PUBG_BASE = "https://api.pubg.com/shards"

HEADERS = {
    "Authorization": f"Bearer {PUBG_API_KEY}",
    "Accept": "application/vnd.api+json"
}


# ── صفحة الـ HTML الرئيسية ──
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# ── API: جلب اسم اللاعب ──
@app.route("/api/player", methods=["GET"])
def get_player():
    player_id = request.args.get("id", "").strip()
    shard     = request.args.get("shard", "steam").strip()

    if not player_id:
        return jsonify({"error": "أدخل الـ Player ID"}), 400

    if not PUBG_API_KEY:
        return jsonify({"error": "PUBG_API_KEY غير موجود في متغيرات البيئة"}), 500

    allowed_shards = ["steam", "psn", "xbox", "kakao", "tournament"]
    if shard not in allowed_shards:
        return jsonify({"error": "منصة غير صحيحة"}), 400

    url = f"{PUBG_BASE}/{shard}/players/{player_id}"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        data = res.json()

        if res.status_code == 404:
            return jsonify({"error": "اللاعب غير موجود — تأكد من الـ ID والمنصة"}), 404

        if res.status_code == 401:
            return jsonify({"error": "الـ API Key غير صحيح أو منتهي"}), 401

        if res.status_code == 429:
            return jsonify({"error": "تجاوزت الحد — انتظر دقيقة وحاول مجدداً"}), 429

        if not res.ok:
            err_title = data.get("errors", [{}])[0].get("title", f"خطأ {res.status_code}")
            return jsonify({"error": err_title}), res.status_code

        name       = data["data"]["attributes"]["name"]
        shard_back = data["data"]["attributes"]["shardId"]

        return jsonify({
            "name":  name,
            "shard": shard_back,
            "id":    player_id
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "انتهت مهلة الاتصال — حاول مجدداً"}), 504

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "فشل الاتصال بـ PUBG API"}), 502

    except Exception as e:
        return jsonify({"error": f"خطأ غير متوقع: {str(e)}"}), 500


# ── Health check لـ Render ──
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
