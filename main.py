from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from TikTokApi import TikTokApi
import os

app = Flask(__name__)

follower_count = {"username": "andyirlofficial", "followers": 0}

def update_followers():
    try:
        with TikTokApi() as api:
            user = api.user(username="andyirlofficial")
            follower_count["followers"] = user.info()["stats"]["followerCount"]
    except Exception as e:
        print("Error fetching TikTok data:", e)

# Run update every 5 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_followers, trigger="interval", seconds=5)
scheduler.start()

@app.route("/followers.json")
def get_followers():
    return jsonify(follower_count)

# Only for local test. Use gunicorn in production (Render).
if __name__ == "__main__":
    update_followers()
    app.run(host="0.0.0.0", port=5000)
