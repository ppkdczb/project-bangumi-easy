from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text
import config
from exts import db
from models import BangumiType2, BangumiEp, BgmCrtCv, BgmCharacter, BgmComment, BgmPersonCv, BgmArticle, BgmUser
import sys
import io
import random
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route("/query/")
def query():
    page = request.args.get('page')
    if page == "" or page is None:
        page = 1
    else:
        page = int(page)
    anime_name = request.args.get('anime_name')
    if anime_name == "" or anime_name is None:
        return redirect(url_for('index'))
    else:
        pagi = BangumiType2.query.filter(BangumiType2.name_cn.like('%' + anime_name + '%')).paginate(page=page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("query.html", ame=ame, paginate=pagi, anime_name=anime_name)

@app.route("/index")
def index():
    random_list = []
    for i in range(9):
        random_num = random.randint(1, 1000)
        random_list.append(BangumiType2.query.order_by(BangumiType2.rating_total.desc()).offset(random_num).first())
    return render_template("index.html", ame=random_list)


@app.route("/popular/")
def popular():
    sort = request.args.get('sort')
    page = request.args.get('page')
    if sort == "" or sort is None:
        sort = 'rating_total'
    if page == "" or page is None:
        page = 1
    else:
        page = int(page)
    if sort == 'rating_total':
        pagi = BangumiType2.query.order_by(BangumiType2.rating_total.desc()).paginate(page = page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("popular.html", ame=ame, sort=sort, paginate=pagi)
    elif sort == 'begintime':
        pagi = BangumiType2.query.order_by(BangumiType2.begin.desc()).paginate(page = page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("popular.html", ame=ame, sort=sort, paginate=pagi)
    elif sort == 'alpha':
        pagi = BangumiType2.query.order_by(BangumiType2.name).paginate(page = page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("popular.html", ame=ame, sort=sort, paginate=pagi)
    return render_template("popular.html")


@app.route("/anime/<int:id>")
def anime(id):
    info = BangumiType2.query.filter_by(bangumi_id=id).first()
    sql = text(
        "SELECT * FROM bgm_character WHERE bgm_character.character_id in (SELECT DISTINCT character_id FROM `bgm-crt-cv` WHERE bangumi_id = %d)" % id)
    conn = db.engine.connect()
    rs = conn.execute(sql)
    characters = []
    for r in rs:
        characters.append(r)
    print(characters)
    return render_template("detail.html", info=info, characters=characters, len=min(len(characters), 8))


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
