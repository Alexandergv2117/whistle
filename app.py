import os
import re
import time
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ["SLACK_USER_TOKEN"])
MY_ID = app.client.auth_test()["user_id"]

GIFS = [
    "https://media.giphy.com/media/yznMzHpdxOpQSrNmE1/giphy.gif",
    "https://media.giphy.com/media/TlMf43T37mdc501iYT/giphy.gif",
    "https://media.giphy.com/media/ZJieMJ372LLjXsInfV/giphy.gif",
]

PATTERN = re.compile(
    r"\bchifl\w*"
    r"|\bsil[bv](?:id|ar|and|at|a\b|e\b)\w*"
    r"|\bpit(?:o|os|ido|idos|azo|azos|ar|ando)\b"
    r"|\bfiu+\b"
    r"|\bwhistl\w*",
    re.IGNORECASE,
)

# So it does not look like a bot: do not always reply, nor repeatedly in the same channel
REPLY_PROBABILITY = 1.0  # 1.0 = always reply; lower it (e.g. 0.7) to skip some
COOLDOWN = 12 * 3600  # minimum seconds between replies in the same channel (12 h)
last_reply = {}  # channel -> time of the last reply

# Allowed channels (comma-separated IDs). If not set, it replies everywhere.
CHANNELS = {c.strip() for c in os.environ.get("SLACK_CHANNEL_ID", "").split(",") if c.strip()}


@app.message(PATTERN)
def reply_with_gif(message, say, logger):
    try:
        if message.get("user") == MY_ID or message.get("bot_id"):
            return
        channel = message.get("channel")
        if CHANNELS and channel not in CHANNELS:
            return
        if random.random() > REPLY_PROBABILITY:
            return
        now = time.time()
        if now - last_reply.get(channel, 0) < COOLDOWN:
            return
        last_reply[channel] = now
        time.sleep(random.uniform(3, 10))
        say(
            blocks=[
                {
                    "type": "image",
                    "image_url": random.choice(GIFS),
                    "alt_text": "whistle",
                }
            ],
        )
    except Exception:
        logger.exception("Could not reply to the message")


@app.event("message")
def ignore_others():
    pass


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
