This project is simply a POC to see how to use a SQL database as backend for logging in a pyramid project.

The idea is to use something like this in pyramid_oereb project, the logger must stay as light as possible and be configurable very easily. Also it should be "plug and play".

The current state uses the logger written in folder `sqlalchemylogger/` and is configured to send both application and apache-like logs to a sqlite DB. If the DB does not exist, it is created at the first use of the logger.

Whe generate apache-like logs using [Paste.Translogger](https://github.com/cdent/paste/blob/master/paste/translogger.py), which is a giant wrapper around the WSGI application.

Everything is configured in `development.ini`.

To run the project:

```shell
make install
make serve
```

to check the logger try:

```shell
curl localhost:6543/
```

you should see the results both on console output and find them in SQL DB:


```shell
sqlite3 logger_db.sqlite3
```

and then


```sql
SELECT * FROM logs;
```

to see only `wsgi` apache-like logs:


```sql
SELECT * FROM logs WHERE logger like 'wsgi';
```

or only `wsgi` logs issued after a given time:

```sql
SELECT * FROM logs WHERE created_at >= '2019-11-13 20:50:00' AND  logger like 'wsgi';
```

