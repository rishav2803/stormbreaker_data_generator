DATASOURCE_TYPES = ["SNOWFLAKE", "POSTGRES", "DATABRICKS", "MSSQL"]
DATASOURCE_ORIGINS = ["WEB", "CLI", "WEB", "CLI"]
COMMON_CONNECTION = {
    "host": "dcs-demo-pgsql.test.com",
    "port": "54309",
    "username": "dbdb",
    "password": "pass",
    "database": "dbtestr",
    "schema": "sample",
}

COMMON_COLUMNS = [
    "first_name",
    "last_name",
    "email",
    "age",
    "id"
]


VALIDATIONS = [
    "count_no_null",
    "count_email",
    "count_isin",
    "max",
]
#add he new constants here
