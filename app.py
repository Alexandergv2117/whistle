import os
import re
import time
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()  # lee las variables del archivo .env

# Token de USUARIO (xoxp-...): los mensajes salen publicados con tu cuenta
app = App(token=os.environ["SLACK_USER_TOKEN"])
MI_ID = app.client.auth_test()["user_id"]

PATRON = re.compile(r"d[oó]nde\s+(est[aá]|qued[oó]|anda).*chiflido", re.IGNORECASE)


@app.message(PATRON)
def responder_chiflido(message, say):
    if message.get("user") == MI_ID:  # no te respondas a ti mismo
        return
    time.sleep(random.uniform(3, 10))  # pequeña pausa para que se vea natural
    say(text="Aquí está el chiflido 😗🎶")


@app.event("message")
def ignorar_otros(body, logger):
    pass


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
