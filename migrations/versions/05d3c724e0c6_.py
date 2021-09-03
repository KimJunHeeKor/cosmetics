"""empty message

Revision ID: 05d3c724e0c6
Revises: cd545ed71f8a
Create Date: 2021-09-03 14:41:26.821546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05d3c724e0c6'
down_revision = 'cd545ed71f8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cur_kw1',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('msg', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('cur_kw2',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('msg', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('brand', sa.String(length=45), nullable=True),
    sa.Column('price', sa.String(length=45), nullable=True),
    sa.Column('ingredients', sa.String(length=45), nullable=True),
    sa.Column('type', sa.String(length=45), nullable=True),
    sa.Column('skintype', sa.String(length=45), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('acc_id', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('jwt', sa.String(length=300), nullable=True),
    sa.Column('token', sa.String(length=300), nullable=True),
    sa.Column('year_of_birth', sa.Integer(), nullable=False),
    sa.Column('marriage', sa.String(length=45), nullable=False),
    sa.Column('childbirth', sa.String(length=45), nullable=False),
    sa.Column('job', sa.String(length=45), nullable=False),
    sa.Column('education', sa.String(length=45), nullable=False),
    sa.Column('hp_no', sa.String(length=45), nullable=False),
    sa.Column('email', sa.String(length=45), nullable=False),
    sa.Column('sex', sa.String(length=10), nullable=False),
    sa.Column('residence', sa.String(length=45), nullable=False),
    sa.Column('nation', sa.String(length=45), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('B_img_cur_rel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skin_prob', sa.String(length=45), nullable=False),
    sa.Column('degree', sa.String(length=45), nullable=False),
    sa.Column('cur_kw1_code', sa.Integer(), nullable=True),
    sa.Column('cur_kw2_code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cur_kw1_code'], ['cur_kw1.code'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['cur_kw2_code'], ['cur_kw2.code'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('login_time', sa.DateTime(), nullable=True),
    sa.Column('logout_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['uid'], ['user_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('survey_cur_rel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ans_code', sa.String(length=45), nullable=False),
    sa.Column('cur_kw1_code', sa.Integer(), nullable=False),
    sa.Column('cur_kw2_code', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cur_kw1_code'], ['cur_kw1.code'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['cur_kw2_code'], ['cur_kw2.code'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('baumann_output',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('dry_oily_score', sa.Integer(), nullable=False),
    sa.Column('sen_res_score', sa.Integer(), nullable=False),
    sa.Column('pig_nopig_score', sa.Integer(), nullable=False),
    sa.Column('wrinkle_tight_score', sa.Integer(), nullable=False),
    sa.Column('dry_lvl', sa.String(length=10), nullable=False),
    sa.Column('oily_lvl', sa.String(length=10), nullable=False),
    sa.Column('sen_lvl', sa.String(length=10), nullable=False),
    sa.Column('pig_lvl', sa.String(length=10), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('img_desc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('full_face', sa.String(length=100), nullable=False),
    sa.Column('oil_paper', sa.String(length=100), nullable=False),
    sa.Column('crop_cheek', sa.String(length=100), nullable=True),
    sa.Column('crop_undereye', sa.String(length=100), nullable=False),
    sa.Column('extract_oilpaper', sa.String(length=100), nullable=True),
    sa.Column('device_type', sa.String(length=45), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('img_output',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('moisture_score', sa.Integer(), nullable=False),
    sa.Column('pore_score', sa.Integer(), nullable=False),
    sa.Column('oily_score', sa.Integer(), nullable=False),
    sa.Column('pigment_score', sa.Integer(), nullable=False),
    sa.Column('moisture_lvl', sa.String(length=10), nullable=False),
    sa.Column('pore_lvl', sa.String(length=10), nullable=False),
    sa.Column('oily_lvl', sa.String(length=10), nullable=False),
    sa.Column('pigment_lvl', sa.String(length=10), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('msg_to_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('msg_type', sa.String(length=45), nullable=False),
    sa.Column('curation_msg', sa.String(length=255), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_rec',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('town', sa.String(length=45), nullable=True),
    sa.Column('air_condition', sa.String(length=45), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('student_env', sa.String(length=45), nullable=True),
    sa.Column('work_env', sa.String(length=45), nullable=True),
    sa.Column('freel_env', sa.String(length=45), nullable=True),
    sa.Column('env_Q1', sa.String(length=45), nullable=False),
    sa.Column('env_Q2', sa.String(length=45), nullable=False),
    sa.Column('env_Q3', sa.String(length=45), nullable=False),
    sa.Column('env_Q4', sa.String(length=45), nullable=False),
    sa.Column('life_Q1', sa.String(length=45), nullable=False),
    sa.Column('life_Q2', sa.String(length=45), nullable=False),
    sa.Column('life_Q3', sa.String(length=45), nullable=False),
    sa.Column('life_Q4', sa.String(length=45), nullable=False),
    sa.Column('life_Q5', sa.String(length=45), nullable=False),
    sa.Column('life_Q6', sa.String(length=45), nullable=False),
    sa.Column('life_Q7', sa.String(length=45), nullable=False),
    sa.Column('life_Q8', sa.String(length=45), nullable=False),
    sa.Column('life_Q9', sa.String(length=45), nullable=False),
    sa.Column('life_Q10', sa.String(length=45), nullable=False),
    sa.Column('dry_Q1', sa.String(length=45), nullable=False),
    sa.Column('dry_Q2', sa.String(length=45), nullable=False),
    sa.Column('dry_Q3', sa.String(length=45), nullable=False),
    sa.Column('dry_Q4', sa.String(length=45), nullable=False),
    sa.Column('dry_Q5', sa.String(length=45), nullable=False),
    sa.Column('dry_Q6', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q1', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q2', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q3', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q4', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q5', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q6', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q7', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q8', sa.String(length=45), nullable=False),
    sa.Column('sensitive_Q9', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q1', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q2', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q3', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q4', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q5', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q6', sa.String(length=45), nullable=False),
    sa.Column('pigment_Q7', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q1', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q2', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q3', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q4', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q5', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q6', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q7', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q8', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q9', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q10', sa.String(length=45), nullable=False),
    sa.Column('wrinkle_Q11', sa.String(length=45), nullable=False),
    sa.Column('etc_Q1', sa.String(length=45), nullable=False),
    sa.Column('etc_Q2', sa.String(length=45), nullable=False),
    sa.Column('etc_Q3', sa.String(length=45), nullable=False),
    sa.Column('etc_Q4', sa.String(length=45), nullable=False),
    sa.Column('etc_Q5', sa.String(length=45), nullable=False),
    sa.Column('etc_Q6', sa.String(length=45), nullable=False),
    sa.Column('etc_Q7', sa.String(length=45), nullable=False),
    sa.Column('etc_Q8', sa.String(length=45), nullable=False),
    sa.Column('etc_Q9', sa.String(length=45), nullable=False),
    sa.Column('etc_Q10', sa.String(length=45), nullable=False),
    sa.Column('etc_Q11', sa.String(length=45), nullable=False),
    sa.Column('etc_Q12', sa.String(length=45), nullable=False),
    sa.Column('etc_Q13', sa.String(length=45), nullable=False),
    sa.Column('etc_Q14', sa.String(length=45), nullable=False),
    sa.Column('etc_Q15', sa.String(length=45), nullable=False),
    sa.Column('etc_Q16', sa.String(length=45), nullable=False),
    sa.Column('etc_Q17', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('total_score_output',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_id', sa.Integer(), nullable=False),
    sa.Column('baumann_skintype', sa.String(length=45), nullable=False),
    sa.Column('total_score', sa.Integer(), nullable=False),
    sa.Column('moisture', sa.Integer(), nullable=False),
    sa.Column('pore', sa.Integer(), nullable=False),
    sa.Column('oily', sa.Integer(), nullable=False),
    sa.Column('pigment', sa.Integer(), nullable=False),
    sa.Column('sensitivity', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['s_id'], ['submit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('total_score_output')
    op.drop_table('survey')
    op.drop_table('product_rec')
    op.drop_table('msg_to_user')
    op.drop_table('img_output')
    op.drop_table('img_desc')
    op.drop_table('baumann_output')
    op.drop_table('survey_cur_rel')
    op.drop_table('submit')
    op.drop_table('log_info')
    op.drop_table('B_img_cur_rel')
    op.drop_table('user_info')
    op.drop_table('product')
    op.drop_table('cur_kw2')
    op.drop_table('cur_kw1')
    # ### end Alembic commands ###
