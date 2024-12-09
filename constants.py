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
    "min", 
    "max", 
    "avg", 
    "sum", 
    # "count_rows", 
    # "count_null", 
    # "count_empty"
]
#add he new constants here
