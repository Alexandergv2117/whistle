import os
import re
import json
import time
import random
import threading
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ["SLACK_USER_TOKEN"])
MY_ID = app.client.auth_test()["user_id"]

def load_gifs(raw):
    """GIF URLs from an env var: a JSON array or a comma-separated list."""
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("["):
        return [str(u).strip() for u in json.loads(raw) if str(u).strip()]
    return [u.strip() for u in raw.split(",") if u.strip()]


GIFS = load_gifs(os.environ.get("GIFS", ""))
if not GIFS:
    raise SystemExit('GIFS is required: a JSON array of URLs, e.g. ["https://.../a.gif"]')

# Random wait (seconds) before replying, so it does not answer instantly
MIN_DELAY = float(os.environ.get("REPLY_DELAY_MIN", 5))
MAX_DELAY = float(os.environ.get("REPLY_DELAY_MAX", 45))
if MIN_DELAY > MAX_DELAY:
    MIN_DELAY, MAX_DELAY = MAX_DELAY, MIN_DELAY

PATTERN = re.compile(
    r"\bchifl\w*"
    r"|\bsil[bv](?:id|ar|and|at|a\b|e\b)\w*"
    r"|\bpit(?:o|os|ido|idos|azo|azos|ar|ando)\b"
    r"|\bfiu+\b"
    r"|\bwhistl\w*",
    re.IGNORECASE,
)

# So it does not look like a bot: do not always reply, nor repeatedly in the same channel
REPLY_PROBABILITY = float(os.environ.get("REPLY_PROBABILITY", 1.0))  # 1.0 = always reply
COOLDOWN = float(os.environ.get("REPLY_COOLDOWN", 7200))  # seconds between replies per channel
last_reply = {}  # channel -> time of the last reply
seen = set()  # (channel, ts) already handled, since Slack may redeliver events
last_gif = None  # avoid sending the same GIF twice in a row

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
        key = (channel, message.get("ts"))
        if key in seen:
            return
        if len(seen) > 1000:
            seen.clear()
        seen.add(key)
        if random.random() > REPLY_PROBABILITY:
            return
        now = time.time()
        if now - last_reply.get(channel, 0) < COOLDOWN:
            return
        last_reply[channel] = now
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        gif = pick_gif()
        # Answer inside the thread if the message was written in one
        thread_ts = message.get("thread_ts")
        # Timer instead of sleep so the handler does not block other messages
        timer = threading.Timer(delay, send_gif, args=(say, gif, thread_ts, logger))
        timer.daemon = True
        timer.start()
    except Exception:
        logger.exception("Could not schedule the reply")


def pick_gif():
    global last_gif
    options = [g for g in GIFS if g != last_gif] or GIFS
    last_gif = random.choice(options)
    return last_gif


def send_gif(say, gif, thread_ts, logger):
    try:
        say(
            blocks=[{"type": "image", "image_url": gif, "alt_text": "whistle"}],
            thread_ts=thread_ts,
        )
    except Exception:
        logger.exception("Could not reply to the message")


@app.event("message")
def ignore_others():
    pass


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
