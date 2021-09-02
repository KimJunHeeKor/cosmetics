from cosmetic import db
from datetime import datetime

class BimgCurRel(db.Model):
    __tablename__ = 'B_img_cur_rel'
    id = db.Column(db.Integer, primary_key=True)
    skin_prob = db.Column(db.String(45), nullable=False, default=None)
    degree = db.Column(db.String(45), nullable=False, default=None)
    cur_kw1_code = db.Column(db.Integer, db.ForeignKey('cur_kw1.code', ondelete='CASCADE'), nullable=True)
    cur_kw2_code = db.Column(db.Integer, db.ForeignKey('cur_kw2.code', ondelete='CASCADE'), nullable=True)

class BaumannOutput(db.Model):
    __tablename__ = 'baumann_output'
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete="CASCADE"), nullable=False)
    dry_oily_score = db.Column(db.Integer, nullable=False)
    sen_res_score = db.Column(db.Integer, nullable=False)
    pig_nopig_score = db.Column(db.Integer, nullable=False)
    wrinkle_tight_score = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class CurKw1(db.Model):
    __tablename__ = 'cur_kw1'
    code = db.Column(db.Integer, primary_key=True, nullable=False)
    msg = db.Column(db.String(45), nullable=False)

class CurKw2(db.Model):
    __tablename__ = 'cur_kw2'
    code = db.Column(db.Integer, primary_key=True, nullable=False)
    msg = db.Column(db.String(45), nullable=False)

class ImgDesc(db.Model):
    __tablename__ = 'img_desc'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete="CASCADE"), nullable=False)
    full_face = db.Column(db.String(100), nullable=False)
    oil_paper = db.Column(db.String(100), nullable=False)
    crop_cheek = db.Column(db.String(100), nullable=True)
    crop_undereye = db.Column(db.String(100), nullable=False)
    extract_oilpaper = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(45), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class ImgOutput(db.Model):
    __tablename__ = 'img_output'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete="CASCADE"), nullable=False)
    moisture_score = db.Column(db.Integer, nullable=False)
    pore_score = db.Column(db.Integer, nullable=False)
    oily_score = db.Column(db.Integer, nullable=False)
    pigment_score = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now) 

class LogInfo(db.Model):
    __tablename__ = 'log_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user_info.id', ondelete='CASCADE'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=True, default=datetime.now)
    logout_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

class MsgToUser(db.Model):
    __tablename__ = 'msg_to_user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete='CASCADE'), nullable=False)
    msg_type = db.Column(db.String(45), nullable=False)
    curation_msg = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now) 

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    brand = db.Column(db.String(45), nullable=True)
    price = db.Column(db.String(45), nullable=True)
    ingredients = db.Column(db.String(45), nullable=True)
    type = db.Column(db.String(45), nullable=True)
    skintype = db.Column(db.String(45), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class ProductRec(db.Model):
    __tablename__ = 'product_rec'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer,  db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now) 

class Submit(db.Model):
    __tablename__ = "submit"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user_info.id', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now) 

class Survey(db.Model):
    __tablename__ = 'survey'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete='CASCADE'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    student_env = db.Column(db.String(45), nullable=True, default=None)
    work_env = db.Column(db.String(45), nullable=True, default=None)
    freel_env = db.Column(db.String(45), nullable=True, default=None)
    env_Q1 = db.Column(db.String(45), nullable=False)
    env_Q2 = db.Column(db.String(45), nullable=False)
    env_Q3 = db.Column(db.String(45), nullable=False)
    env_Q4 = db.Column(db.String(45), nullable=False)
    life_Q1 = db.Column(db.String(45), nullable=False)
    life_Q2 = db.Column(db.String(45), nullable=False)
    life_Q3 = db.Column(db.String(45), nullable=False)
    life_Q4 = db.Column(db.String(45), nullable=False)
    life_Q5 = db.Column(db.String(45), nullable=False)
    life_Q6 = db.Column(db.String(45), nullable=False)
    life_Q7 = db.Column(db.String(45), nullable=False)
    life_Q8 = db.Column(db.String(45), nullable=False)
    life_Q9 = db.Column(db.String(45), nullable=False)
    life_Q10 = db.Column(db.String(45), nullable=False)
    dry_Q1 = db.Column(db.String(45), nullable=False)
    dry_Q2 = db.Column(db.String(45), nullable=False)
    dry_Q3 = db.Column(db.String(45), nullable=False)
    dry_Q4 = db.Column(db.String(45), nullable=False)
    dry_Q5 = db.Column(db.String(45), nullable=False)
    dry_Q6 = db.Column(db.String(45), nullable=False)
    sensitive_Q1 = db.Column(db.String(45), nullable=False)
    sensitive_Q2 = db.Column(db.String(45), nullable=False)
    sensitive_Q3 = db.Column(db.String(45), nullable=False)
    sensitive_Q4 = db.Column(db.String(45), nullable=False)
    sensitive_Q5 = db.Column(db.String(45), nullable=False)
    sensitive_Q6 = db.Column(db.String(45), nullable=False)
    sensitive_Q7 = db.Column(db.String(45), nullable=False)
    sensitive_Q8 = db.Column(db.String(45), nullable=False)
    sensitive_Q9 = db.Column(db.String(45), nullable=False)
    pigment_Q1 = db.Column(db.String(45), nullable=False)
    pigment_Q2 = db.Column(db.String(45), nullable=False)
    pigment_Q3 = db.Column(db.String(45), nullable=False)
    pigment_Q4 = db.Column(db.String(45), nullable=False)
    pigment_Q5 = db.Column(db.String(45), nullable=False)
    pigment_Q6 = db.Column(db.String(45), nullable=False)
    pigment_Q7 = db.Column(db.String(45), nullable=False)
    wrinkle_Q1 = db.Column(db.String(45), nullable=False)
    wrinkle_Q2 = db.Column(db.String(45), nullable=False)
    wrinkle_Q3 = db.Column(db.String(45), nullable=False)
    wrinkle_Q4 = db.Column(db.String(45), nullable=False)
    wrinkle_Q5 = db.Column(db.String(45), nullable=False)
    wrinkle_Q6 = db.Column(db.String(45), nullable=False)
    wrinkle_Q7 = db.Column(db.String(45), nullable=False)
    wrinkle_Q8 = db.Column(db.String(45), nullable=False)
    wrinkle_Q9 = db.Column(db.String(45), nullable=False)
    wrinkle_Q10 = db.Column(db.String(45), nullable=False)
    wrinkle_Q11 = db.Column(db.String(45), nullable=False)
    etc_Q1 = db.Column(db.String(45), nullable=False)
    etc_Q2 = db.Column(db.String(45), nullable=False)
    etc_Q3 = db.Column(db.String(45), nullable=False)
    etc_Q4 = db.Column(db.String(45), nullable=False)
    etc_Q5 = db.Column(db.String(45), nullable=False)
    etc_Q6 = db.Column(db.String(45), nullable=False)
    etc_Q7 = db.Column(db.String(45), nullable=False)
    etc_Q8 = db.Column(db.String(45), nullable=False)
    etc_Q9 = db.Column(db.String(45), nullable=False)
    etc_Q10 = db.Column(db.String(45), nullable=False)
    etc_Q11 = db.Column(db.String(45), nullable=False)
    etc_Q12 = db.Column(db.String(45), nullable=False)
    etc_Q13 = db.Column(db.String(45), nullable=False)
    etc_Q14 = db.Column(db.String(45), nullable=False)
    etc_Q15 = db.Column(db.String(45), nullable=False)
    etc_Q16 = db.Column(db.String(45), nullable=False)
    etc_Q17 = db.Column(db.String(45), nullable=False)

class SurveyCurRel(db.Model):
    __tablename__ = 'survey_cur_rel'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ans_code = db.Column(db.String(45), nullable=False)
    cur_kw1_code = db.Column(db.Integer, db.ForeignKey('cur_kw1.code', ondelete='CASCADE'), nullable=False)
    cur_kw2_code = db.Column(db.Integer, db.ForeignKey('cur_kw2.code', ondelete='CASCADE'), nullable=False)

class TotalScoreOutput(db.Model):
    __tablename__ = 'total_score_output'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('submit.id', ondelete='CASCADE'), nullable=False)
    baumann_skintype = db.Column(db.String(45), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    moisture = db.Column(db.Integer, nullable=False)
    pore = db.Column(db.Integer, nullable=False)
    oily = db.Column(db.Integer, nullable=False)
    pigment = db.Column(db.Integer, nullable=False)
    sensitivity = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    acc_id = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    jwt = db.Column(db.String(300), nullable=True, default=None)
    token = db.Column(db.String(300), nullable=True, default=None)
    year_of_birth = db.Column(db.Integer, nullable=False)
    marriage = db.Column(db.String(45), nullable=False)
    childbirth = db.Column(db.String(45), nullable=False)
    job = db.Column(db.String(45), nullable=False)
    education = db.Column(db.String(45), nullable=False)
    hp_no = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.now)