# Whistle bot 😗🎶

Bot de Slack que responde automáticamente cuando alguien pregunta por el "chiflido".

Escucha los mensajes de los canales donde estás y, si detecta una pregunta como
*"¿Dónde está el chiflido?"*, *"dónde quedó el chiflido"* o *"donde anda el chiflido"*,
responde con:

> Aquí está el chiflido 😗🎶

## Cómo funciona

- Usa [Slack Bolt para Python](https://slack.dev/bolt-python/) en **Socket Mode** (no necesita URL pública).
- Usa un **token de usuario** (`xoxp-...`), así que las respuestas se publican con tu cuenta, no con la de un bot.
- Espera entre 3 y 10 segundos antes de responder para que parezca natural.
- Ignora tus propios mensajes para no responderse a sí mismo.
- El patrón detectado (sin importar mayúsculas ni acentos) es:
  `dónde + (está | quedó | anda) ... chiflido`.

## Requisitos

- Python 3.9+
- Una app de Slack con Socket Mode activado

## Configuración de la app de Slack

1. Crea una app en <https://api.slack.com/apps> (*From scratch*).
2. En **Socket Mode**, actívalo y genera un **App-Level Token** con el scope
   `connections:write` → es tu `SLACK_APP_TOKEN` (`xapp-...`).
3. En **OAuth & Permissions**, añade los siguientes **User Token Scopes**:
   - `channels:history`, `groups:history`, `im:history`, `mpim:history` (leer mensajes)
   - `chat:write` (publicar como tú)
4. En **Event Subscriptions**, actívalo y suscríbete a los eventos de usuario
   (*Subscribe to events on behalf of users*): `message.channels`, `message.groups`,
   `message.im`, `message.mpim`.
5. Instala la app en tu workspace y copia el **User OAuth Token** → es tu
   `SLACK_USER_TOKEN` (`xoxp-...`).

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install slack_bolt python-dotenv
```

## Variables de entorno

Copia el archivo de ejemplo y completa tus tokens:

```bash
cp .env.example .env
```

| Variable           | Descripción                                          |
| ------------------ | ---------------------------------------------------- |
| `SLACK_USER_TOKEN` | Token de usuario (`xoxp-...`), publica con tu cuenta |
| `SLACK_APP_TOKEN`  | Token de app (`xapp-...`) para Socket Mode           |

> ⚠️ Nunca subas tu `.env` al repositorio: contiene credenciales que dan acceso a tu cuenta.

## Uso

```bash
python3 app.py
```

Deja el proceso corriendo; el bot responderá mientras esté activo.

## Personalización

Todo está en `app.py`:

- **Frase a detectar:** modifica la expresión regular `PATRON`.
- **Respuesta:** cambia el texto en `say(text=...)`.
- **Retraso:** ajusta el rango en `time.sleep(random.uniform(3, 10))`.
