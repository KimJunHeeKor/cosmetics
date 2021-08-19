from config.default import *

db = {
    'user' : 'ncyc',
    'password' : 'ncyc0078',
    'host' : '14.39.220.155',
    'port' : '3306',
    'database' : 'curation_service'
}

SQLALCHEMY_DATABASE_URI =  f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'f\xabx\xe7\xca\x8eC\x87\xb8\xa47\x85\xea4\\d'