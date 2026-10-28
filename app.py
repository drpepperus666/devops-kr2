# KR2: Шаломеенко А.А.
import os
import socket

import redis
from flask import Flask, request

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True,
)


@app.route("/health")
def health():
    return "ok\n"


@app.route("/")
def index():
    count = redis_client.incr("hits")
    container = socket.gethostname()[:12]
    student = os.getenv("STUDENT", "unknown")
    return f"KR2 | {student} | container {container} | hits: {count}\n"


@app.route("/whoami")
def whoami():
    def header(name):
        value = request.headers.get(name)
        return value if value is not None else "none"

    scheme = header("X-Forwarded-Proto")
    client = header("X-Real-IP")
    host = header("Host")
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
