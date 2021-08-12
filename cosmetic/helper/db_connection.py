import pymysql

__host_ip__ = '14.39.220.155'
__user__ = 'ncyc'
__password__ = 'ncyc0078'
__db__ = 'curation_service'


def db_connect(host, user, password, db, sql):
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