from faker import Faker
from sqlalchemy.orm import Session
from app.models.dataset_model import Dataset
from app.schemas.common_schema import UserRole
from random import randint
import faker
fake = Faker()



def create_dataset(session: Session, datasource_id: UserRole) -> str:
    """
    Generates and inserts random workspace data into the database.

    Args:
        session (Session): SQLAlchemy session object.
        user_id (str): ID of the user who owns the workspace.
        user_role (UserRole): Role of the user.

    Returns:
        str: ID of the created workspace.
    """


    datasetname="testpublic."+fake.word()

    dataset = Dataset(
        name=datasetname,
        metadata={},
        data_source_id=datasource_id,
    )

    session.add(dataset)
    session.flush()

    return dataset.id