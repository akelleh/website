import datetime
import json
import boto3
import os


class WebLogger(object):
    def __init__(self, s3_bucket, s3_path, log_file_path='.'):
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        self.log_file = LogFile(self.get_current_filename(), log_file_path)
        self.s3_bucket = s3_bucket
        self.s3_path = s3_path
        self.s3_client = boto3.client('s3')
        self.log_file_path = log_file_path

    def get_current_filename(self):
        now = datetime.datetime.now()
        return "{}-{}-{}_{}:{}.log".format(now.year,
                                       now.month,
                                       now.day,
                                       now.hour,
                                       15*int(now.minute/15))

    def log(self, event):
        filename = self.get_current_filename()
        if filename != self.log_file.filename:
            if not self.log_file.empty:
                self.upload_and_remove_log()
            self.log_file = LogFile(filename, self.log_file_path)

        self.log_file.append_event(event)

    def upload_and_remove_log(self):
        response = self.s3_client.put_object(Body=open(self.log_file.full_path, 'rb'),
                                             Bucket=self.s3_bucket,
                                             Key=os.path.join(self.s3_path,
                                                              self.log_file.filename))
        print(response)
        os.remove(self.log_file.full_path)


class LogFile(object):
    def __init__(self, filename, file_path):
        self.filename = filename
        self.full_path = os.path.join(file_path, filename)
        self.empty = True

    def append_event(self, event):
        self.empty = False
        with open(self.full_path, 'a') as fp:
            fp.write(json.dumps(event)+'\n')