from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from TikTokApi import TikTokApi
import os

app = Flask(__name__)

# Replace with your real sessionid
SESSIONID = os.environ.get("TIKTOK_SESSIONID", "your-session-id-here")

follower_data = {"username": "andyirlofficial", "followers": 0}

def update_followers():
    global follower_data
    try:
        api = TikTokApi()
        api._get_sessionid = lambda: SESSIONID  # Inject sessionid manually

        user = api.user(username="andyirlofficial")
        stats = user.info(full_response=True)
        count = stats['userInfo']['stats']['followerCount']

        follower_data["followers"] = count
        print("Updated follower count:", count)

    except Exception as e:
        print("Error fetching follower count:", e)

scheduler = BackgroundScheduler()
scheduler.add_job(update_followers, 'interval', seconds=5)
scheduler.start()

@app.route("/followers.json")
def get_follower_json():
    return jsonify(follower_data)

if __name__ == "__main__":
    update_followers()
    app.run(host="0.0.0.0", port=5000)
