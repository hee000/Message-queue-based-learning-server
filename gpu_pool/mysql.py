import pymysql 
from env import MYSQL_SERVER_IP, MYSQL_SERVER_PORT, MYSQL_SERVER_USER, MYSQL_SERVER_PASSWORD, MESSAGE_COLUMNS
from typing import Optional

class MysqlManager():
    __host       = None
    __port       = None
    __user       = None
    __password   = None
    __database   = None
    session    = None
    connection = None

    def __init__(self, host=MYSQL_SERVER_IP, port=MYSQL_SERVER_PORT, user=MYSQL_SERVER_USER, password=MYSQL_SERVER_PASSWORD, database='ai_train'):
        self.__host     = host
        self.__user     = user
        self.__port     = port
        self.__password = password
        self.__database = database
        
    def open(self, db:bool=True):
        db = self.__database if db else None
        cnx = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__password, database=db, charset='utf8')
        self.connection = cnx
        self.session    = cnx.cursor()

    def close(self) -> None:
        self.session.close()
        self.connection.close()
        

class MysqlServerManager(MysqlManager):
    def __init__(self, host=MYSQL_SERVER_IP, port=MYSQL_SERVER_PORT, user=MYSQL_SERVER_USER, password=MYSQL_SERVER_PASSWORD, database='ai_train'):
        super().__init__(host, port, user, password, database)

    def create_database(self):
        sql = 'create database IF NOT EXISTS ai_train;'
        
        self.open(db=False)
        self.session.execute(sql)
        self.close()

    def create_table(self):
        message = 'create table IF NOT EXISTS message(id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, '

        for msg in MESSAGE_COLUMNS:
            if msg == 'id':
                continue

            if msg == 'pushed':
                message += 'pushed bool DEFAULT FALSE);'
                continue
            
            message += f'{msg} varchar(255), '

        sqls = [message,
                '''create table IF NOT EXISTS error_message(
                    id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    message_id int(10) NOT NULL,
                    error_log LONGTEXT
                );'''
            ]

        self.open()
        for sql in sqls:
            self.session.execute(sql)
        self.close()

class MysqlClientManager(MysqlManager):
    def __init__(self, host=MYSQL_SERVER_IP, port=MYSQL_SERVER_PORT, user=MYSQL_SERVER_USER, password=MYSQL_SERVER_PASSWORD, database='ai_train'):
        super().__init__(host, port, user, password, database)
    
    def select(self, message_id: int) -> tuple[any]:
        result = tuple()
        sql = f'SELECT * FROM message WHERE id = {message_id}'

        self.open()
        self.session.execute(sql)
        result = self.session.fetchone()
        self.close()

        return result

    def update(self) -> tuple[bool, int]:
        complete = False
        message_id = -1
        seclect_query = f'SELECT * FROM message WHERE pushed = 0 ORDER BY id ASC limit 1 FOR UPDATE;'

        self.open()
        try:
            self.connection.begin()
            self.session.execute(seclect_query)
            result = self.session.fetchone()
            if result and len(result) != 0:
                message_id = result[0]
                update_query = f'UPDATE message SET pushed = 1 WHERE id = {message_id}'
                self.session.execute(update_query)
                complete = True
            self.connection.commit()
        except:
            self.connection.rollback()
            complete = False
        self.close()

        return complete, message_id

    def insert_error_log(self, message_id:int, error_log:str):
        sql = 'INSERT error_message (message_id, error_log) VALUES (%s, %s)'

        self.open()
        self.session.execute(sql, (message_id, error_log))
        self.connection.commit()
        self.close()

class MysqlCamperManager(MysqlManager):
    def __init__(self, host=MYSQL_SERVER_IP, port=MYSQL_SERVER_PORT, user=MYSQL_SERVER_USER, password=MYSQL_SERVER_PASSWORD, database='ai_train'):
        super().__init__(host, port, user, password, database)

    def insert(self, json: dict):
        keys = f'{tuple(json.keys())}'.replace('\'', '')
        values = tuple(json.values())
        sql = f'INSERT message {keys} VALUES {values}'

        self.open()
        self.session.execute(sql)
        self.connection.commit()
        self.close()
    
    def message(self, message_id:Optional[int] = None) -> list[dict[str:any]]:
        result = []
        sql =  f'SELECT * FROM message WHERE id = {message_id}' if message_id != None else 'SELECT * FROM message'

        self.open()
        self.session.execute(sql)
        columns = self.session.description 
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.session.fetchall()]
        self.close()

        return result
    
    def error_message(self, message_id:Optional[int] = None) -> list[dict[str:any]]:
        result = []
        sql =  f'SELECT * FROM error_message WHERE id = {message_id}' if message_id != None else 'SELECT * FROM error_message'

        self.open()
        self.session.execute(sql)
        columns = self.session.description 
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.session.fetchall()]
        self.close()

        return result