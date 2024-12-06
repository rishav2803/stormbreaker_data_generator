from sqlalchemy.orm import Session
from app.models.data_source_model import DataSource
from app.schemas.common_schema import UserRole
from random import randint

from faker import Faker

fake=Faker()



def create_datasource(session: Session, workspace_id: UserRole, user_id: UserRole) -> str:

    # datasource_name=["TEST_SQL","TEST_POSTGRES","TEST_DATABRICKS","TEST_AZURESQL"]
    # print(fake.words()[0])
    # ksbvjbw
    datasource_name="TEST_DATASOURCE_"+fake.words()[0]
    datasource_Type=["SNOWFLAKE","POSTGRES","DATABRICKS","MSSQL"]
    datasource_origin=["WEB","CLI","WEB","CLI"]
    common_connection={"host": "dcs-demo-pgsql.test.com", "port": "54309", "username": "dbdb", "password": "pass", "database": "dbtestr", "schema": "sample"}

    random_idx=randint(0,3)
    datasource = DataSource(
        name=datasource_name,
        type=datasource_Type[random_idx],
        connection=common_connection,
        is_interactive=True if datasource_origin[random_idx]=="WEB" else False,
        origin=datasource_origin[random_idx],
        workspace_id=workspace_id,
        user_id=user_id,
    )

    session.add(datasource)
    session.flush()

    return datasource.id