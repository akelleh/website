import datetime
import json
import boto3
import os
import MySQLdb.connections
import logging
import pandas as pd


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

    def list_logs(self):
        response = self.s3_client.list_objects(Bucket=self.s3_bucket,
                                               Prefix=self.s3_path)
        logs = response.get('Contents', [])
        while response.get('IsTruncated', False):
            try:
                marker = logs[-1].get('Key')
                response = self.s3_client.list_objects(Bucket=self.s3_bucket,
                                                       Prefix=self.s3_path,
                                                       Marker=marker)
                logs += response.get('Contents', [])
            except:
                break
        return [log.get('Key') for log in logs]

    def get_newest_log(self):
        logs = self.list_logs()
        date_format = '%Y-%m-%d_%H:%M.log'
        log_dates = sorted([(datetime.datetime.strptime(os.path.split(log)[-1], date_format), log) for log in logs])
        newest_log = log_dates[-1][1]
        return newest_log

    def download_log(self, log_path):
        self.s3_client.download_file(self.s3_bucket,
                                     log_path,
                                     os.path.join(self.log_file_path, os.path.split(log_path)[-1]))


class LogFile(object):
    def __init__(self, filename, file_path):
        self.filename = filename
        self.full_path = os.path.join(file_path, filename)
        self.empty = True

    def append_event(self, event):
        self.empty = False
        with open(self.full_path, 'a') as fp:
            fp.write(json.dumps(event)+'\n')

    def read_lines(self, n=1000):
        buffer = []
        for line in open(os.path.join(self.full_path), 'r'):
            buffer.append(line)
            if len(buffer) >= n:
                yield buffer
                buffer = []
        if len(buffer) > 0:
            yield buffer


class LightClient(MySQLdb.connections.Connection):
    def query_and_iterate(self, query):
        self.query(query)
        result = self.use_result()
        row = result.fetch_row()
        while row:
            yield row
            row = result.fetch_row()

    def insert_dataframe(self, df, table):
        try:
            value_string = ', '.join(['%s' for _ in range(len(df.columns))])
            columns = ', '.join([col_name for col_name in df.columns])
            cursor = self.cursor()
            cursor.executemany(
                               """INSERT IGNORE INTO {} ({}) VALUES ({})""".format(table, columns, value_string),
                               df.values.tolist())
            self.commit()
            cursor.close()
        except Exception as e:
            print(e)
            cursor.close()


def import_logs():
    logging.info("Importing.")
    log_file_path = './tmp'

    # download the latest log (should be more careful, but don't care too much about losing files),
    # e.g. failing to backfill the gap if there's a long service failure
    logger = WebLogger(s3_bucket='aws-website-adamkelleher-q9wlb',
                       s3_path='pageviews',
                       log_file_path=log_file_path)
    newest_log = logger.get_newest_log()
    logger.download_log(newest_log)
    logging.info("downloaded: " + newest_log)

    # Create the logfile object, and load its contents into MySQL
    logfile = LogFile(os.path.split(newest_log)[-1],
                      log_file_path)
    sql_username = os.environ['MYSQL_USERNAME']
    sql_password = os.environ['MYSQL_PASSWORD']
    sql_server = os.environ['MYSQL_SERVER_ADDRESS']
    sql_database = os.environ['MYSQL_DATABASE']
    sql_client = LightClient(sql_server,
                             sql_username,
                             sql_password,
                             sql_database)
    for lines in logfile.read_lines():
        buffer = pd.DataFrame([json.loads(line) for line in lines])
        sql_client.insert_dataframe(buffer, 'pageviews')
        logging.info("Inserted buffer.")


def backfill_logs():
    logging.info("Importing.")
    log_file_path = './tmp'

    # download the latest log (should be more careful, but don't care too much about losing files),
    # e.g. failing to backfill the gap if there's a long service failure
    logger = WebLogger(s3_bucket='aws-website-adamkelleher-q9wlb',
                       s3_path='pageviews',
                       log_file_path=log_file_path)
    logs = logger.list_logs()
    for log in logs:
        logger.download_log(log)
        logging.info("downloaded: " + log)

        # Create the logfile object, and load its contents into MySQL
        logfile = LogFile(os.path.split(log)[-1],
                          log_file_path)
        sql_username = os.environ['MYSQL_USERNAME']
        sql_password = os.environ['MYSQL_PASSWORD']
        sql_server = os.environ['MYSQL_SERVER_ADDRESS']
        sql_database = os.environ['MYSQL_DATABASE']
        sql_client = LightClient(sql_server,
                                 sql_username,
                                 sql_password,
                                 sql_database)
        for lines in logfile.read_lines():
            buffer = pd.DataFrame([json.loads(line) for line in lines])
            sql_client.insert_dataframe(buffer, 'pageviews')
            logging.info("Inserted buffer.")
