# datadog-mysql-profiler-metrics
MySQL Table Level Metrics for Datadog in Python

## Requirements

### Datadog Keys:

Create API and APP keys:
- https://app.datadoghq.com/account/settings#api

Check out the API Documentation:
- https://docs.datadoghq.com/api/?lang=python#post-timeseries-points

### Python Packages:

```
$ pip install mysqlclient
$ pip install datadog
```

## MySQL Sys Schema:

The sys schema objects can be used for typical tuning and diagnosis use cases:
- https://dev.mysql.com/doc/refman/8.0/en/sys-schema.html

```
mysql> select * from sys.`x$schema_table_statistics` where total_latency > 0\G
*************************** 1. row ***************************
     table_schema: foo
       table_name: bar
    total_latency: 3730128452604
     rows_fetched: 3929224
    fetch_latency: 1998830290976
    rows_inserted: 19967
   insert_latency: 1731298161628
     rows_updated: 0
   update_latency: 0
     rows_deleted: 0
   delete_latency: 0
 io_read_requests: 14
          io_read: 972
  io_read_latency: 51442220
io_write_requests: 43
         io_write: 414182
 io_write_latency: 1079346324
 io_misc_requests: 76
  io_misc_latency: 92505469736
```

## Datadog Timeseries API

The metrics end-point allows you to post time-series data that can be graphed on Datadog’s dashboards:
- https://docs.datadoghq.com/api/?lang=python#post-timeseries-points

```
# Submit multiple metrics
api.Metric.send([{
    'metric': 'my.series',
    'points': 15
}, {
    'metric': 'my1.series',
    'points': 16
}])
```

## Map MySQL to JSON

Map the returned data to json:

```
mysql_querydata = cursor.fetchall()

json_data=[]

for row_data in mysql_querydata:
    json_data.append(dict(zip(row_headers, row_data)))
```

Preview the data:

```
>>> print(json_data)
[{'rows_inserted': 19967, }, {'rows_updated': 0}]
```

## Map Json to Datadog Metrics:

```
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
```

preview data:

```
>>> print(metrics)
[{'metric': 'mysql.custom_metric.foo.io_misc_requests', 'points': Decimal('93'), 'host': 'datadog-mysql', 'tags': ['mysql:performance_data']},..]
```

## Screenshots:

Metrics:

<img width="754" alt="image" src="https://user-images.githubusercontent.com/30043398/61129616-0f0c2200-a4b5-11e9-9a02-4ab1ce2821a6.png">

Dashboard:

<img width="1400" alt="image" src="https://user-images.githubusercontent.com/30043398/61129752-614d4300-a4b5-11e9-9858-3ada60a0e4c4.png">
