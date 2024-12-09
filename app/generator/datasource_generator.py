from sqlalchemy.orm import Session
from app.models.data_source_model import DataSource
from app.schemas.common_schema import UserRole
from random import randint
from constants import DATASOURCE_TYPES,DATASOURCE_ORIGINS,COMMON_CONNECTION

from faker import Faker

fake = Faker()

def create_datasource(session: Session, workspace_id: str, user_id: str, num_sources: int) -> list[str]:
    """
    Creates multiple data sources and returns their IDs.
    """
    data_source_ids = []

    for _ in range(num_sources):
        datasource_name = "TEST_DATASOURCE_" + fake.words()[0]
        random_idx = randint(0, len(DATASOURCE_TYPES) - 1)

        datasource = DataSource(
            name=datasource_name,
            type=DATASOURCE_TYPES[random_idx],
            connection=COMMON_CONNECTION,
            is_interactive=True if DATASOURCE_ORIGINS[random_idx] == "WEB" else False,
            origin=DATASOURCE_ORIGINS[random_idx],
            workspace_id=workspace_id,
            user_id=user_id,
        )

        session.add(datasource)
        session.flush()  # Assigns an ID to the datasource

        data_source_ids.append(datasource.id)

    return data_source_ids

