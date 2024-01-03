import subprocess as sp
from env import CWD, MYSQL_SERVER_PORT, MYSQL_SERVER_USER, MYSQL_SERVER_PASSWORD

def subprocess(command: str) -> sp.CompletedProcess[str]:
    return sp.run(command, capture_output=True, text=True, shell=True)

def start_server() -> None:
    check_installation('mysql-server')

    check_config()

    subprocess(f'cp {CWD}/gpu_pool/cnf/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf')

    print('mysql-server 실행 중...')

    subprocess('usermod -d /var/lib/mysql/ mysql')

    server = subprocess('service mysql start')
    if server.stderr:
        print ('mysql-server를 실행하지 못했습니다. 터미널 로그는 다음과 같습니다. \n', server.stderr)
        raise Exception('mysql-server 실행 실패')
    else:
        user_check = sp.run(['mysql', '-u', 'root'], input="use mysql;\nselect user, host from user;\nexit", capture_output=True, text=True)
        if MYSQL_SERVER_USER not in user_check.stdout:
            sp.run(['mysql', '-u', 'root'], input=f"create user '{MYSQL_SERVER_USER}'@'%' identified by '{MYSQL_SERVER_PASSWORD}';\ngrant all privileges on *.* to '{MYSQL_SERVER_USER}'@'%';\nflush privileges;\nexit", capture_output=True, text=True)

def check_config() -> None:
    config_path = f'{CWD}/gpu_pool/cnf/mysqld.cnf'
    port = f'\nport = {MYSQL_SERVER_PORT}'

    with open(config_path, 'r') as file:
        if file.readlines()[-1] == '##':
            with open(config_path, 'a') as file:
                file.write(port)

def check_installation(kind: str) -> None:
    if kind == 'pymysql':
        command_c = 'pip3 show pymysql'
        command_i = 'pip3 install pymysql --root-user-action=ignore'
    elif kind == 'mysql-server':
        command_c = 'mysql --version'
    elif kind == 'git':
        command_c = 'pip3 show gitpython'
        command_i = 'pip3 install gitpython --root-user-action=ignore'
    else:
        raise Exception(f'지정오류')
    
    print(f'{kind} 설치 확인 중...')
    check = subprocess(command_c)
    if check.stderr:
        if kind == 'mysql-server':
            print(f'{kind} 는 따로 설치가 필요합니다. 설치 후 유저 권한 부여와 외부 접속 허용 설정이 요구됩니다.')
            raise Exception(f'{kind} 설치되지 않음')
        
        print(f'{kind} 설치되어 있지 않습니다. 설치를 시작합니다.')

        print(f'{kind} 설치 중...')
        install = subprocess(command_i)
        if install.stderr and 'WARNING: Running pip as the \'root\' user can result in broken permissions' not in install.stderr:
            print(f'{kind} 설치에 실패했습니다. 터미널 로그는 다음과 같습니다. \n', install.stderr)
            raise Exception(f'{kind} 설치 실패')