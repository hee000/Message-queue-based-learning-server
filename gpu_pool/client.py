import time
import utils
utils.check_installation('git')
from mysql import MysqlClientManager
import git
from env import CWD, MESSAGE_COLUMNS, ARGS_EXCEPTION, BRANCH_INDEX, TRAIN_INDEX

def start():
    utils.subprocess('git config credential.helper cache')
    utils.subprocess('git config credential.helper \'cache --timeout=1036800\'')
    utils.subprocess('git pull')

    sql = MysqlClientManager()

    print('client 실행')
    while True:
        print('작업 새로고침')

        message_id = -1

        try:
            complete, message_id = sql.update()
            if complete:
                args_value = sql.select(message_id)

                branch = args_value[BRANCH_INDEX]
                train_path = args_value[TRAIN_INDEX]

                repo = git.Repo.init(path=CWD)

                repo.git.checkout('develop')
                if branch != 'develop':
                    try:
                        repo.git.branch('-D', branch)
                    except:
                        pass
                repo.git.remote('update')
                repo.git.remote('prune', 'origin')
                repo.remotes.origin.pull()
                repo.git.checkout(branch)

                args = ''
                for idx, name in enumerate(MESSAGE_COLUMNS):
                    if name in ARGS_EXCEPTION:
                        continue
                    args += f'--{name} {args_value[idx]} '

                utils.subprocess(f'pip install -r {CWD}/requirements.txt')

                print('학습 중')
                train = utils.subprocess(f'python {CWD}/{train_path} {args}')
                if train.stderr and 'UserWarning: Argument \'interpolation\' of type int is deprecated since 0.13 and will be removed in 0.15' not in train.stderr:
                    sql.insert_error_log(message_id, train.stderr)
                    print(f'학습 중 에러 발생. error_message에서 {message_id}를 참조바랍니다.')
                else:
                    print('학습 완료')
        except Exception as e:
            sql.insert_error_log(message_id, e)
            print(f'에러 발생. error_message에서 {message_id}를 참조바랍니다.')

        time.sleep(60)

if __name__ == "__main__":
    start()