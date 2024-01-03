import os

CWD = os.getcwd()

MYSQL_SERVER_IP =
MYSQL_SERVER_PORT =
MYSQL_SERVER_USER =
MYSQL_SERVER_PASSWORD =

MESSAGE_FILE_PATH =

# id, branch, train_path, pushed의 위치를 수정하지 마세요.
MESSAGE_COLUMNS = ['id', 'branch', 'train_path',
                   
                  '...',

                  'pushed']

# 이하 수정 x
ARGS_EXCEPTION = ['id', 'branch', 'train_path', 'pushed']
BRANCH_INDEX = 1
TRAIN_INDEX = 2