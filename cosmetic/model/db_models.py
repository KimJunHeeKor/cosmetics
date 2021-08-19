from .. import db
from datetime import datetime

class BaumannCurRel(db.Model):
    __tablename__ = 'Baumann_cur_rel'
    Baumann_cur_rel_id = db.Column(db.Integer, primary_key=True)
    Baumann_output_id = db.Column(db.Integer, db.ForeignKey('BaumannOutput.id', ondelete='CASCADE'),nullable=False)
    cur_kw1_id = db.Column(db.Integer, db.ForeignKey('cur_kw1.id', ondelete='CASCADE'), nullable=True)
    cur_kw2_id = db.Column(db.Integer, db.ForeignKey('cur_kw2.id', ondelete='CASCADE'), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

class BaumannOuput(db.Model):
    __tablename__ = 'Baumann_output'
    Baumann_output_id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    survey_id = db.Column(db.Integer, nullable=False)
    Baumann_type = db.Column(db.String(45), nullable=False)
    Baumann_dry_oily = db.Column(db.String(45), nullable=False)
    Baumann_sen_res = db.Column(db.String(45), nullable=False)
    Baumann_pig_nonpig = db.Column(db.String(45), nullable=False)
    Baumann_wrinkle_tight = db.Column(db.String(45), nullable=False)
    Baumann_total_score = db.Column(db.Integer, nullable=False)
    Baumann_dry_oily_score = db.Column(db.Integer, nullable=False)
    Baumann_sen_res_score = db.Column(db.Integer, nullable=False)
    Baumann_pig_nopig_score = db.Column(db.Integer, nullable=False)
    Baumann_wrinkle_tight_score = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
class CaptureEnv(db.Model):
    __tablename__ = 'capture_env'
    capture_env_id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'),nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    device_type = db.Column(db.String(45), nullable=False)

class CurKw1(db.Model):
    __tablename__ = 'cur_kw1'
    cur_kw1_id = db.Column(db.Integer, primary_key=True, nullable=False)
    cur_kw1_msg = db.Column(db.String(45), nullable=False)

class CurKw2(db.Model):
    __tablename__ = 'cur_kw2'
    cur_kw2_id = db.Column(db.Integer, primary_key=True, nullable=False)
    cur_kw2_msg = db.Column(db.String(45), nullable=False)

# class ImgCurRel(db.Model):
#     __tablename__ = 'img_ur_rel'
#     pass

#TODO : 나머지 DB table 넣기
