from flask import Flask, g
from db import RedisClient


app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Flask ProxyPool</h2>'

@app.route('/random')
def get_random_proxy():
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()