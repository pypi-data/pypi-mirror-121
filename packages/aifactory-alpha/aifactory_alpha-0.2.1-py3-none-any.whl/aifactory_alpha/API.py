from aifactory_alpha.Authentification import AFAuth, AFCrypto
from aifactory_alpha.constants import *
from datetime import datetime
import logging
import os
import requests
import http
import json


class AFContest:
    _summary_ = None
    logger = None
    auth_method = None
    user_token = None
    user_email = None
    task_id = None
    model_name_prefix = None
    encrypt_mode = None
    def __init__(self, auth_method=AUTH_METHOD.USERINFO, user_token=None,
                 user_email=None, model_name_prefix=None, task_id=None,
                 log_dir="./log/", debug=False, encrypt_mode=True,
                 submit_url=SUBMISSION_DEFAULT_URL, auth_url=AUTH_DEFAULT_URL):
        self.auth_method = auth_method
        self.refresh_token = user_token
        self.user_email = user_email
        self.model_name_prefix = model_name_prefix
        self.task_id = task_id
        self.set_log_dir(log_dir)
        self.debug = debug
        self.encrypt_mode = int(encrypt_mode)
        self.submit_url = submit_url
        self.auth_url = auth_url
        self.auth_manager = AFAuth(user_email, task_id, self.logger, token=user_token, password=None,
                                   auth_method=auth_method, encrypt_mode=encrypt_mode, auth_url=auth_url, debug=debug)

    def set_log_dir(self, log_dir: str):
        self.log_dir = os.path.abspath(log_dir)
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        if not os.path.isdir(self.log_dir):
            raise AssertionError("{} is not a directory.".format(self.log_dir))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(module)s:%(levelname)s: %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def set_user_email(self, email: str):
        self.user_email = email
        self.auth_manager.set_user_email(email)

    def set_task_id(self, task_id: int):
        self.task_id = task_id
        self.auth_manager.set_task_id(task_id)

    def set_model_name_prefix(self, model_name_prefix: str):
        self.model_name_prefix = model_name_prefix

    def reset_logger(self, prefix=LOG_TYPE.SUBMISSION):
        cur_log_file_name = prefix+datetime.now().__str__().replace(" ", "-").replace(":", "-").split(".")[0]+".log"
        log_path = os.path.join(self.log_dir, cur_log_file_name)
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.log_path = log_path

    def _is_file_valid_(self, file_path):
        if not os.path.exists(file_path):
            self.logger.error("File {} not found.".format(file_path))
            return False
        elif os.path.getsize(file_path) > FILE_STATUS.MAX_FILE_SIZE:
            self.logger.error(FileTooLargeError.ment)
            return False
        elif file_path.split('.')[-1] not in FILE_TYPE.available_file_extensions:
            self.logger.error(FileTypeNotAvailable.ment)
            return False
        return True

    def _send_file_(self, auth_token, file_path, submit_url=SUBMISSION_DEFAULT_URL, num_trial=0):
        headers = {'token': auth_token,
                   'file-type': file_path.split('.')[-1]}
        response = None
        with open(file_path, 'rb') as f:
            response = requests.post(submit_url+'/submit', files={'file': f}, headers=headers)
        if self.debug:
            self.logger.info('Response from auth server: {}'.format(response.text))
        if response.text == SUBMIT_RESPONSE.TOKEN_NOT_VALID:
            self.logger.info("Token not valid. Starting authentification again.")
            auth_token = self.auth_manager.get_token(refresh=True)
            return self._send_file_(auth_token, file_path, submit_url, num_trial+1)
        elif response.text == SUBMIT_RESPONSE.DB_NOT_AVAILABLE:  # if the system has a problem.
            self.logger.error(SubmitServerError.ment)
            raise(SubmitServerError)
        elif response.status_code == http.HTTPStatus.OK:
            response_params = json.loads(response.text)
            self.logger.info("Submission completed. Please check the leader-board for scoring result.")
            self.logger.info("You have been submitted for {} times.".format(response_params['submit_number']))
            self.logger.info("The model name was recorded as {}.".format(response_params['model_name']))
        return response

    def submit(self, file_path):
        # This method submit the answer file to the server.
        def _fail_(self, _status_):
            self.logger.error("Submission Failed.")
            print("Please have a look at the logs in '{}' for more details.".format(self.log_path))
            return _status_
        def _succeed_(self, _status_):
            self.logger.info("Submission was successful.")
            print("Results are recorded in the log file '{}'.".format(self.log_path))
            return _status_
        self.reset_logger(LOG_TYPE.SUBMISSION)
        status = SUBMIT_RESULT.FAIL_TO_SUBMIT
        if not self._is_file_valid_(file_path):
            return _fail_(self, status)
        auth_token = self.auth_manager.get_token(refresh=True)
        if auth_token is False:
            return _fail_(self, status)
        response = self._send_file_(auth_token, file_path)
        status = SUBMIT_RESULT.SUBMIT_SUCCESS
        return _succeed_(self, status)

    def release(self):
        # This method submit the answer file and the code to the server.
        pass

    def summary(self):
        _summary_ = ">>> Contest Information <<<\n"
        _summary_ += self.auth_manager.summary()
        if self.model_name_prefix is not None:
            _summary_ += "Model Name Prefix: {}\n".format(self.model_name_prefix)
        return _summary_


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_email', '-u', help='Example) myid@myemail.domain.com', dest='user_email')
    parser.add_argument('--task_id', '-t', help='Example) 3000', dest='task_id')
    parser.add_argument('--file', '-f', nargs='+', help='Example) answer.csv', dest='file')
    parser.add_argument('--debug', '-d', type=bool, help='Example) False', default=True, dest='debug')
    parser.add_argument('--submit_url', help='Example) http://submit.aifactory.solutions',
                        default=SUBMISSION_DEFAULT_URL, dest='submit_url')
    parser.add_argument('--auth_url', help='Example) http://auth.aifactory.solutions',
                        default=AUTH_DEFAULT_URL, dest='auth_url')
    parser.add_argument('--log_dir', help='Example) http://auth.aifactory.solutions',
                        default="./log", dest='log_dir')
    args = parser.parse_args()
    if args.debug:
        user_email = 'user0@aifactory.space' if args.user_email is None else args.user_email
        task_id = '3000' if args.task_id is None else args.task_id
        files = ['./sample_data/sample_answer.csv'] if args.file is None else args.file
        c = AFContest(user_email=user_email, task_id=task_id, debug=args.debug,
                      submit_url=args.submit_url, auth_url=args.auth_url, log_dir=args.log_dir)
        c.summary()
        c.submit(files[0])
    else:
        c = AFContest(user_email=args.user_email, task_id=args.task_id, debug=args.debug,
                      submit_url=args.submit_url, auth_url=args.auth_url, log_dir=args.log_dir)
        c.summary()
        c.submit(args.file[0])

