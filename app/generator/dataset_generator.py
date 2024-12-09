from faker import Faker
from sqlalchemy.orm import Session
from app.models.dataset_model import Dataset
from app.schemas.common_schema import UserRole
from random import randint
import faker

fake = Faker()

def create_dataset(session: Session, num_datasets: int, data_source_ids: list[str]) -> list[list[str]]:
    """
    Creates multiple datasets for a given data source and returns their IDs and names.

    Args:
        session (Session): SQLAlchemy session object.
        num_datasets (int): Number of datasets to create.
        data_source_ids: All the data source ids created

    Returns:
        list[list[str]]: List of [dataset_id, dataset_name] for the created datasets.
    """
    dataset_details = []

    for data_source_id in data_source_ids:
        for _ in range(num_datasets):
            dataset_name = "testpublic." + fake.word()

            dataset = Dataset(
                name=dataset_name,
                metadata={},
                data_source_id=data_source_id,
            )

            session.add(dataset)
            session.flush()  # Assigns an ID to the dataset

            dataset_details.append([dataset.id, dataset_name])

    return dataset_details