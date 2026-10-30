# Whistle bot 😗🎶

A Slack bot that replies with a random GIF when someone mentions the "chiflido" (whistle).
It runs in Socket Mode and posts **as your user** (`xoxp-` token).

## 1. Configure the Slack app

1. Go to <https://api.slack.com/apps> → **Create New App** → **From a manifest**.
2. Pick your workspace, paste the contents of [`manifest.json`](manifest.json) (JSON tab) and create the app.
3. **Basic Information → App-Level Tokens → Generate Token and Scopes**: add the
   `connections:write` scope and generate it. Copy the `xapp-...` token → `SLACK_APP_TOKEN`.
4. **Install App → Install to Workspace** and allow it. Copy the **User OAuth Token**
   (`xoxp-...`) → `SLACK_USER_TOKEN`.

Optional: to limit the bot to certain channels, copy their IDs (channel name → **View channel
details** → bottom of **About**) into `SLACK_CHANNEL_ID`, comma-separated.

## 2. Environment variables

| Variable           | Required | Description                                          |
| ------------------ | -------- | ---------------------------------------------------- |
| `SLACK_USER_TOKEN` | yes      | `xoxp-...` user token                                |
| `SLACK_APP_TOKEN`  | yes      | `xapp-...` app-level token                           |
| `SLACK_CHANNEL_ID` | no       | Channel ID(s), comma-separated. Empty = all channels |
| `GIFS`             | yes      | GIF URLs as a JSON array (comma-separated also works) |
| `REPLY_DELAY_MIN`  | no       | Min seconds to wait before replying (default `5`)    |
| `REPLY_DELAY_MAX`  | no       | Max seconds to wait before replying (default `45`)   |
| `REPLY_PROBABILITY`| no       | Chance of replying, 0–1 (default `1`)                |
| `REPLY_COOLDOWN`   | no       | Seconds between replies per channel (default `7200`, 2 h)    |

> ⚠️ Never commit `.env`: the user token gives access to your account.

## 3. Run after cloning

```bash
git clone https://github.com/Alexandergv2117/whistle.git
cd whistle
cp .env.example .env   # fill in the tokens
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## 4. Production (Docker Compose)

Uses the prebuilt image `ghcr.io/alexandergv2117/whistle:latest`. Compose reads the tokens
from a `.env` file next to `compose.yml`.

```bash
cp .env.example .env   # fill in the tokens
docker compose up -d
docker compose logs -f whistle
```

To update: `docker compose pull && docker compose up -d`.
