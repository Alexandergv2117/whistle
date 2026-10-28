import os
import re
import time
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ["SLACK_USER_TOKEN"])
MI_ID = app.client.auth_test()["user_id"]

GIFS = [
    "https://media.giphy.com/media/yznMzHpdxOpQSrNmE1/giphy.gif",
    "https://media.giphy.com/media/TlMf43T37mdc501iYT/giphy.gif",
    "https://media.giphy.com/media/ZJieMJ372LLjXsInfV/giphy.gif",
]

PATRON = re.compile(
    r"\bchifl\w*"
    r"|\bsil[bv](?:id|ar|and|at|a\b|e\b)\w*"
    r"|\bpit(?:o|os|ido|idos|azo|azos|ar|ando)\b"
    r"|\bfiu+\b"
    r"|\bwhistl\w*",
    re.IGNORECASE,
)

# Para que no parezca un bot: no se responde siempre ni seguido en el mismo canal
PROBABILIDAD = 1.0  # 1.0 = responde siempre; bájalo (p. ej. 0.7) para saltarte algunas
ENFRIAMIENTO = 12 * 3600  # segundos mínimos entre respuestas en un mismo canal (12 h)
ultima_respuesta = {}  # canal -> momento de la última respuesta


@app.message(PATRON)
def responder_chiflido(message, say, logger):
    try:
        if message.get("user") == MI_ID or message.get("bot_id"):
            return
        if random.random() > PROBABILIDAD:
            return
        canal = message.get("channel")
        ahora = time.time()
        if ahora - ultima_respuesta.get(canal, 0) < ENFRIAMIENTO:
            return
        ultima_respuesta[canal] = ahora
        time.sleep(random.uniform(3, 10))
        say(
            blocks=[
                {
                    "type": "image",
                    "image_url": random.choice(GIFS),
                    "alt_text": "chiflido",
                }
            ],
        )
    except Exception:
        logger.exception("No se pudo responder al mensaje")


@app.event("message")
def ignorar_otros():
    pass


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
