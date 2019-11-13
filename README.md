This project is simply a POC to see how to use a SQL database as backend for logging in a pyramid project.

The idea is to use something like this in pyramid_oereb project, the logger must stay as light as possible and be configurable very easily. Also it should be "plug and play".

The current state uses the logger written in folder `sqlalchemylogger/` and is configured to send both application and apache-like logs to a sqlite DB. If the DB does not exist, it is created at the first use of the logger.

Everything is configured in `development.ini`.

To run the project:

```shell
make install
make serve
```

