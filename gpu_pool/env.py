# import os

# CWD = os.getcwd()

# MYSQL_SERVER_IP = '10.28.224.116'
# MYSQL_SERVER_PORT = 30014
# MYSQL_SERVER_USER = 'cv11'
# MYSQL_SERVER_PASSWORD = 'cv11'

# MESSAGE_FILE_PATH = 'file_dir'

# # id, brach, train, pushed는 수정하지 말 것
# MESSAGE_COLUMNS = ['id', 'branch', 'train', 'camper_id', 'name', 'seed', 'epoch', 'dataset', 'augmentation',
#               'resize', 'batch_size', 'valid_batch_size', 'model', 'optimizer',
#               'lr', 'val_ratio', 'criterion', 'lr_decay_step', 'log_interval',
#               'patience', 'data_dir', 'model_dir', 'pushed'
#               ]
# ARGS_EXCEPTION = ['id', 'branch', 'train', 'pushed']
# BRANCH_INDEX = 1
# TRAIN_INDEX = 2

import os

CWD = os.getcwd()

MYSQL_SERVER_IP = '10.28.224.116'
MYSQL_SERVER_PORT = 30014
MYSQL_SERVER_USER = 'cv11'
MYSQL_SERVER_PASSWORD = 'cv11'

MESSAGE_FILE_PATH = 'file_dir'

# id, brach, train, pushed의 위치는 고정해주세요
MESSAGE_COLUMNS = ['id', 'branch', 'train_path', 'camper_id', 'name', 'seed', 'epoch', 'dataset', 'augmentation',
              'resize', 'batch_size', 'valid_batch_size', 'model', 'optimizer',
              'lr', 'val_ratio', 'criterion', 'lr_decay_step', 'log_interval',
              'patience', 'data_dir', 'model_dir', 'pushed'
              ]
ARGS_EXCEPTION = ['id', 'branch', 'train_path', 'pushed']
BRANCH_INDEX = 1
TRAIN_INDEX = 2