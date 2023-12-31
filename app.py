import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
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
from werkzeug.security import generate_password_hash, check_password_hash

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.secret_key = 'kdjklfjkd87384hjdhjh'


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
        pagi = BangumiType2.query.filter(BangumiType2.name_cn.like(
            '%' + anime_name + '%')).paginate(page=page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("query.html", ame=ame, paginate=pagi, anime_name=anime_name)


@app.route("/index")
def index():
    random_list = []
    for i in range(9):
        random_num = random.randint(1, 1000)
        random_list.append(BangumiType2.query.order_by(
            BangumiType2.rating_total.desc()).offset(random_num).first())
    art = BgmArticle.query.order_by(BgmArticle.article_date.desc()).limit(5)
    return render_template("index.html", ame=random_list, art=art)

class User:
    def __init__(self, user_name, user_id):
        self.user_name = user_name
        self.id = user_id


@app.before_request
def before_request():
    user_name = session.get('user_name')
    if user_name:
        g.user = User(user_name, session.get('user_id'))
    else:
        g.user = None


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
        pagi = BangumiType2.query.order_by(BangumiType2.rating_total.desc()).paginate(
            page=page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("popular.html", ame=ame, sort=sort, paginate=pagi)
    elif sort == 'begintime':
        pagi = BangumiType2.query.order_by(BangumiType2.begin.desc()).paginate(
            page=page, per_page=15, error_out=False)
        ame = pagi.items
        return render_template("popular.html", ame=ame, sort=sort, paginate=pagi)
    elif sort == 'alpha':
        pagi = BangumiType2.query.order_by(BangumiType2.name).paginate(
            page=page, per_page=15, error_out=False)
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
    return render_template("detail.html", info=info, characters=characters, len=min(len(characters), 8))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        user_name = form.get('user_name')
        user_password = form.get('user_password')
        print(user_password)
        print("here")
        session.pop('user_name', None)
        session.pop('user_id', None)
        user = BgmUser.query.filter_by(user_name=user_name).first()
        if user and user.user_password == user_password:
            flash('登录成功！', 'success')
            session['user_name'] = user_name
            session['user_id'] = user.user_id
            return redirect(url_for('index'))
        else:
            flash('用户名或密码不正确。', 'danger')
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('user_name', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        user_name = form.get('user_name')
        user_password = form.get('user_password')
        user_address = form.get('user_address')
        print(user_name)
        print(user_password)
        print(user_address)
        existing_user = BgmUser.query.filter_by(user_name=user_name).first()

        if existing_user:
            flash('用户已存在，请登录。', 'info')
            return redirect(url_for('login'))

        # hashed_password = generate_password_hash(
        #    user_password, method='sha256')
        new_user = BgmUser(
            user_name=user_name, user_password=user_password, user_address=user_address)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录。', 'success')
        return redirect(url_for('login'))

    # 如果是 GET,返回 register 模板
    return render_template("register.html")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/topic/<int:id>", methods=["POST", "GET"])
def topic(id):
    if request.method == "POST":
        form = request.form
        comment_text = form.get('comment')
        if comment_text == "":
            return redirect(url_for('topic', id=id))
        comment_date = datetime.now()
        comment_user_id = session.get('user_id')
        comment_article_id = id
        new_comment = BgmComment(comment_text=comment_text, comment_date=comment_date,
                                 comment_user_id=comment_user_id, comment_article_id=comment_article_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('topic', id=id))
    else:
        art = BgmArticle.query.filter_by(article_id=id).first()
        comment = BgmComment.query.filter_by(comment_article_id=id).all()
        name = BgmUser.query.filter_by(user_id=art.article_user_id).first()
        users = []
        for i in range(len(comment)):
            users.append(BgmUser.query.filter_by(
                user_id=comment[i].comment_user_id).first().user_name)

        return render_template("topic.html", id=id, art=art, comments=comment, name=name, users=users,
                               num_comment=len(comment))


@app.route("/discuss/<int:id>")
def discuss(id):
    page = id
    pagi = BgmArticle.query.order_by(BgmArticle.article_date.desc()).paginate(
        page=page, per_page=15, error_out=False)
    dis = pagi.items
    print("YES")
    return render_template("discuss.html", dis=dis, paginate=pagi)


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(port=5500)
