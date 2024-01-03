import argparse
import json
import argparse
import pprint
import utils
from env import MESSAGE_FILE_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='use "python %(prog)s -h --help" for more information',formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        'mode',
        metavar='Select one among server, client, push, message, error',
        type=str,
        help='''
        server - Run mysql server
        client - Run the message queue based auto-learning client
        push - Push message to queue
        message - Check message list
        error - Check error message list
        '''
    )
    parser.add_argument(
        '-i',
        '--id',
        metavar='int',
        type=int,
        help='message or error_message id (default = None / None: ALL)'
    )

    args = parser.parse_args()
    mode = args.mode

    utils.check_installation('pymysql')
    from mysql import MysqlCamperManager

    sql = MysqlCamperManager()

    if mode == 'server':
        import server
        server.start()
    elif mode == 'client':
        import client
        client.start()
    elif mode == 'push':
        with open(MESSAGE_FILE_PATH, 'r') as f:
            json_object = json.load(f)
            sql.insert(json=json_object)
            print("메시지 푸시 완료")
    elif mode == 'message':
        result = sql.message(args.id)
        pprint.pprint(result)
    elif mode == 'error':
        result = sql.error_message(args.id)
        pprint.pprint(result)
    else:
        print('올바른 인자를 입력해주세요.')