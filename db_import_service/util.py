import datetime
import json
import boto3
import os
import MySQLdb


def download_and_insert_pageviews():


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
                               """INSERT INTO {} ({}) VALUES ({})""".format(table, columns, value_string),
                               df.values.tolist())
            self.commit()
            cursor.close()
        except Exception as e:
            print(e)
            cursor.close()
