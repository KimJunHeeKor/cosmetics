from config.default import *

SQLALCHEMY_DATABASE_URI =  f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'f\xabx\xe7\xca\x8eC\x87\xb8\xa47\x85\xea4\\d'