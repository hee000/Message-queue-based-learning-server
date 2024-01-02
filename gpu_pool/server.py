import utils
from mysql import MysqlServerManager

def start():
    utils.start_server()

    sql = MysqlServerManager()
    sql.create_database()
    sql.create_table()

    print("mysql server 실행 완료")
    
if __name__ == "__main__":
    start()