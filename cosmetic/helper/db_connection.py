import pymysql

HOST_IP = '14.39.220.155'
USER = 'ncyc'
PASSWORD = 'ncyc0078'
DB_NAME = 'curation_service'

def db_connect(sql, host=HOST_IP, user=USER, password=PASSWORD, db=DB_NAME):
    try:
        # mysql 연결    
        con = pymysql.connect(host=host, user=user, password=password,
        db=db, charset='utf8')

        #Connection으로부터 cursor생성
        cur = con.cursor()

        #SQL문 실행 및 Fetch
        cur.execute(sql)

        # 데이타 fetch
        rows = cur.fetchall()

        # db연결 종료
        con.close()
        
        return rows
    except Exception as err:
        print(f'[DB connection ERROR] : {err}')