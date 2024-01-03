# Message-queue-based-learning-server

Message-queue-based-learning-server는 분산되어 있는 gpu 서버들이 메시지 큐를 통해 자동으로 학습할 수 있는 환경을 제공합니다.

## Project Structure

```
${PROJECT}
├── gpu_pool
├── ai 관련 폴더
|   ├── train.py
|   └── ... 등
├── ai 관련 파일
├── ... 등
├── README.md
└── requirements.txt
```

## Getting Started

### Requirements

Server 경우:
- MySQL Server (MySQL >= 8.0) 사전 설치 필요
  - ```apt-get install mysql-server```

### Usage

- **사용 전에 env.py 수정이 필요합니다.**

#### Server

아래의 코드를 실행하기전 env.py에 비어 있는 항목을 모두 기입한 후 실행해야합니다.
ai_stages에서 서버를 할당받을 때 주어진 포트 번호 중 한 개를 선택하여 사용하시기 바랍니다.
```
python gpu_pool server
```

#### Client
- 첫 실행은 foreground로 하여 반복되는 git checkout 작업을 위해 git 아이디와 액세스 토큰을 입력해야 합니다. 아이디와 액세스 토큰은 11일 동안 캐싱 됩니다. 이 기간 동안 background 실행이 가능합니다.
- 11일이 지난 이후엔 다시 foreground로 실행하여 아이디와 액세스 토큰을 입력해야 합니다.
```
# foreground
python gpu_pool client

# background
nohup python gpu_pool client &
```

#### Message

```
# Push message to queue
python gpu_pool push

#Check message list
python gpu_pool message
# or
python gpu_pool message -id 2


#Check error message list
python gpu_pool error
# or
python gpu_pool error -id 3
```

### Example

#### env

```
# MySQL Server 관련 
MYSQL_SERVER_IP = '10.28.xxx.xxx'
MYSQL_SERVER_PORT = 30034
MYSQL_SERVER_USER = 'hee'
MYSQL_SERVER_PASSWORD = 'password'

# 큐에 푸시하려는 메시지를 작성한 파일의 주소
MESSAGE_FILE_PATH = './message.json'

# 메시지 큐에 담을 내용
# id, branch, train_path, pushed의 위치를 수정하지 마세요.
MESSAGE_COLUMNS = ['id', 'branch', 'train_path',
                    'name', 'seed', 'epoch', 'dataset', 'augmentation',
                    'criterion', 'batch_size',

                    ...

                    'model', 'optimizer',
                    'pushed'
                  ]


# 이하 수정 x
ARGS_EXCEPTION = ['id', 'branch', 'train_path', 'pushed']
BRANCH_INDEX = 1
TRAIN_INDEX = 2
```

#### message

```
# ./message.json
# branch, train_path 항목 필수 // id, pushed 항목은 x
# env.py의 MESSAGE_COLUMNS을 바탕으로 작성

{
  "branch": "develop",   # or commit ex) e6084c6b
  "train_path": "./ai_folder/train.py"

  "name": "test_name",
  "seed": "42",
  "epoch": "1",
  "dataset": "MaskBaseDataset",
  "augmentation": "BaseAugmentation",
  "resize": "128 96",
  "batch_size": "64",
  "valid_batch_size": "1000",
  "model": "BaseModel",
  "optimizer": "SGD",
  "lr": "1e-3",
  "val_ratio": "0.2",
  "criterion": "cross_entropy",
  "lr_decay_step": "20",
  "log_interval": "20",
  "patience": "5",
  "data_dir": "test_data_dir",
  "model_dir": "test_model_dir"
}
```
