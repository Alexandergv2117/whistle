# Whistle bot 😗🎶

A Slack bot that automatically replies with a random GIF when someone mentions the "chiflido" (whistle).

It listens to the messages in the channels you are in and, when it detects a whistle-related word
(*chiflido*, *silbidito*, *pitido*, *fiu*, *whistle*...), it replies with a random GIF from a list.

## How it works

- Uses [Slack Bolt for Python](https://slack.dev/bolt-python/) in **Socket Mode** (no public URL needed).
- Uses a **user token** (`xoxp-...`), so replies are posted with your account, not as a bot.
- Waits 3 to 10 seconds before replying so it looks natural.
- Ignores your own messages and other bots' messages.
- Does not reply every time, so it does not look like a bot:
  - `REPLY_PROBABILITY`: chance of replying (1.0 = always).
  - `COOLDOWN`: minimum time between replies in the same channel (12 h by default).
- Optionally restricts replies to specific channels (see `SLACK_CHANNEL_ID`).
- Matching is case-insensitive and based on word stems, so it covers all forms:
  - `chifl…`: chiflido, chiflidito, chifle, chiflar...
  - `silb…` / `silv…`: silbido, silbidito, silvidito, silbar, silbato...
  - `pit…`: pito, pitido, pitazo, pitar...
  - `fiu`, `whistle`.

## Requirements

- Python 3.9+ (or Docker)
- A Slack app with Socket Mode enabled

## Slack app setup

1. Create an app at <https://api.slack.com/apps> (*From scratch*).
2. Under **Socket Mode**, enable it and generate an **App-Level Token** with the
   `connections:write` scope → this is your `SLACK_APP_TOKEN` (`xapp-...`).
3. Under **OAuth & Permissions**, add the following **User Token Scopes**:
   - `channels:history`, `groups:history`, `im:history`, `mpim:history` (read messages)
   - `chat:write` (post as you)
4. Under **Event Subscriptions**, enable it and subscribe to user events
   (*Subscribe to events on behalf of users*): `message.channels`, `message.groups`,
   `message.im`, `message.mpim`.
5. Install the app in your workspace and copy the **User OAuth Token** → this is your
   `SLACK_USER_TOKEN` (`xoxp-...`).

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Copy the example file and fill in your tokens:

```bash
cp .env.example .env
```

| Variable           | Description                                                                            |
| ------------------ | -------------------------------------------------------------------------------------- |
| `SLACK_USER_TOKEN` | User token (`xoxp-...`), posts with your account                                       |
| `SLACK_APP_TOKEN`  | App token (`xapp-...`) for Socket Mode                                                 |
| `SLACK_CHANNEL_ID` | Optional. Channel ID(s) (`C0123456789`), comma-separated. If empty, replies everywhere |

> ⚠️ Never commit your `.env` file: it contains credentials that give access to your account.

## Usage

```bash
python3 app.py
```

Keep the process running; the bot replies while it is active.

## Docker

The `Dockerfile` is multi-stage (dependencies are built in one stage, only the virtualenv and
code are copied to the final image) and runs as an unprivileged user.

```bash
docker build -t whistle-bot:latest .
docker run -d --name whistle --env-file .env whistle-bot:latest
```

`compose.yml` runs a prebuilt image with a hardened configuration (read-only filesystem, no
capabilities, `no-new-privileges`, resource limits). It does not build the image and does not
load `.env`, so provide the tokens as environment variables (for example by adding an
`env_file: .env` entry to the service).

```bash
docker compose up -d
```

### Published image (GitHub Actions)

The workflow in `.github/workflows/docker-publish.yml` builds the image and publishes it to
GitHub Container Registry (`ghcr.io/<owner>/<repo>`):

- Push to `main` → tags `latest` and `sha-<commit>`.
- Tag `vX.Y.Z` → tag `X.Y.Z`.
- Pull requests → build only, nothing is pushed.

To use it, set `image:` in `compose.yml` to that name, for example
`ghcr.io/<owner>/<repo>:latest`.

## Customization

Everything lives in `app.py`:

- **Words to detect:** edit the `PATTERN` regular expression.
- **GIFs:** add public links to the `GIFS` list (format `https://media.giphy.com/media/<id>/giphy.gif`).
- **Reply frequency:** adjust `REPLY_PROBABILITY` and `COOLDOWN`.
- **Delay:** change the range in `time.sleep(random.uniform(3, 10))`.
