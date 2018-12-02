import dash
import dash_core_components as dcc
import dash_html_components as html
import MySQLdb.connections
import os
import pandas as pd


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


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

    def get_pageview_ts(self):
        query = """
                SELECT 
                    DATE(FROM_UNIXTIME(ts)) t, COUNT(user_id)
                FROM
                    pageviews
                WHERE DATE(FROM_UNIXTIME(ts)) > '2018-01-01'
                GROUP BY t
                ORDER BY t DESC
                """
        data = []
        for row in self.query_and_iterate(query):
            data.append(row[0])

        df = pd.DataFrame(data, columns=['t', 'pageviews'])
        return df

    def get_uv_ts(self):
        query = """
                SELECT 
                    DATE(FROM_UNIXTIME(ts)) t, COUNT(DISTINCT user_id)
                FROM
                    pageviews
                WHERE DATE(FROM_UNIXTIME(ts)) > '2018-01-01'
                GROUP BY t
                ORDER BY t DESC
                """
        data = []
        for row in self.query_and_iterate(query):
            data.append(row[0])

        df = pd.DataFrame(data, columns=['t', 'uvs'])
        return df

def get_client():
    sql_username = os.environ['MYSQL_USERNAME']
    sql_password = os.environ['MYSQL_PASSWORD']
    sql_server = os.environ['MYSQL_SERVER_ADDRESS']
    sql_database = os.environ['MYSQL_DATABASE']
    sql_client = LightClient(sql_server,
                             sql_username,
                             sql_password,
                             sql_database)
    return sql_client