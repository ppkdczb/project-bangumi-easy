from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text
import config
from exts import db
from models import BangumiType2, BangumiEp, BgmCrtCv, BgmCharacter, BgmPersonCv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/query/<int:bangumi_id>')
def query(bangumi_id):
    rs = BangumiType2.query.filter_by(bangumi_id=bangumi_id)
    for r in rs:
        print(r.name_cn)
    return 'ok'


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/popular")
def popular():
    return render_template("popular.html")


@app.route("/anime/<int:id>")
def anime(id):
    info = BangumiType2.query.filter_by(bangumi_id=id).first()
    sql = text("SELECT * FROM bgm_character WHERE bgm_character.character_id in (SELECT DISTINCT character_id FROM `bgm-crt-cv` WHERE bangumi_id = %d)" % id )
    conn = db.engine.connect()
    rs = conn.execute(sql)
    characters = []
    for r in rs:
        characters.append(r)
    print(characters)
    return render_template("detail.html", info=info, characters=characters, len = min(len(characters), 5))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/topic/<int:id>")
def topic(id):
    return render_template("topic.html", id=id)


@app.route("/discuss")
def discuss():
    return render_template("discuss.html")


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == '__main__':
    app.run()
