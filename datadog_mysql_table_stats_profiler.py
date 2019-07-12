from datadog import initialize, api
from time import time
from socket import gethostname
import MySQLdb as mysql
import json
import os

DB_HOST=os.environ['DB_HOST']
DB_USER=os.environ['DB_USER']
DB_PASS=os.environ['DB_PASS']
DB_DATABASE='sys'
MY_HOSTNAME = gethostname()

TAGS = ['mysql:performance_data']

options = {
    'app_key': os.environ['DATADOG_APP_KEY'],
    'api_key': os.environ['DATADOG_API_KEY']
}

def get_mysql_data(hostname, username, password, database):
    json_data=[]
    db = mysql.connect(hostname, username, password, database)
    cursor = db.cursor()
    cursor.execute("select * from sys.`x$schema_table_statistics` where total_latency > 0")
    row_headers=[x[0] for x in cursor.description]
    row_data = cursor.fetchall()
    db.close()
    for mysql_row in row_data:
        json_data.append(dict(zip(row_headers, mysql_row)))
    return json_data

def datadog_metrics_mapper(payload, hostname, tags):
    metrics = []
    for each in payload:
        table_name = each['table_name']
        for k in each.keys():
            if type(each[k]) == str:
                pass
            else:
                metrics.append({
                    'metric': 'mysql.custom_metric.{}.{}'.format(table_name, k),
                    'points': each[k],
                    'host': hostname,
                    'tags': tags
                })
    return metrics

# get mysql data
json_data = get_mysql_data(DB_HOST, DB_USER, DB_PASS, DB_DATABASE)

# map data to metrics mapper
metrics = datadog_metrics_mapper(json_data, MY_HOSTNAME, TAGS)

# ship to datadog
initialize(**options)
api.Metric.send(metrics)
