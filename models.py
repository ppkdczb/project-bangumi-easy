# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from exts import db

class BangumiType2(db.Model):
    __tablename__ = 'bangumi__type2'
    __table_args__ = (
        db.Index('name', 'name', 'name_cn'),
    )

    bangumi_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False)
    name_cn = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    officialSite = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False)
    begin = db.Column(db.Date, nullable=False, index=True, server_default=db.FetchedValue())
    rating_total = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    rating_score = db.Column(db.Numeric(4, 2), nullable=False, server_default=db.FetchedValue())
    info = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    summary = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)


class BangumiEp(db.Model):
    __tablename__ = 'bangumi_ep'
    __table_args__ = (
        db.Index('airdate', 'airdate', 'sort'),
        db.Index('B_bangumi_id', 'B_bangumi_id', 'sort')
    )

    ep_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    sort = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False)
    name_cn = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False)
    duration = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    duration_hour = db.Column(db.Integer, nullable=False)
    duration_min = db.Column(db.Integer, nullable=False)
    duration_sec = db.Column(db.Integer, nullable=False)
    airdate = db.Column(db.Date, nullable=False)
    desc = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    B_bangumi_id = db.Column(db.Integer, nullable=False)


class BgmCrtCv(db.Model):
    __tablename__ = 'bgm-crt-cv'

    primary_key = db.Column(db.Integer, primary_key=True)
    bangumi_id = db.Column(db.Integer, nullable=False)
    character_id = db.Column(db.Integer, nullable=False)
    person_id = db.Column(db.Integer, nullable=False)


class BgmCharacter(db.Model):
    __tablename__ = 'bgm_character'
    __table_args__ = (
        db.Index('name', 'name', 'name_cn'),
    )

    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    name_cn = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    cover = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    info = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    detail = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)


class BgmPersonCv(db.Model):
    __tablename__ = 'bgm_person__cv'

    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False)
    name_cn = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    cover = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    info = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    detail = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
