from faker import Faker
from sqlalchemy.orm import Session
from app.models.column_model import Column
from constants import COMMON_COLUMNS

fake = Faker()

def create_data_set_columns(session: Session, dataset_details: list[list[str]]) -> dict[str, list[list[str]]]:
    """
    Creates columns for generated data sets and returns a mapping of data_set_id to column details.

    Args:
        session (Session): SQLAlchemy session object.
        data_set_ids (list[str]): All the data set IDs created.

    Returns:
        dict[str, list[list[str]]]: A mapping of data_set_id to a list of [column_id, column_name].
    """

    data_set_to_columns = {}

    for dataset_detail in dataset_details:
        data_set_id, data_set_name = dataset_detail
        combined_key = f"{data_set_id}/{data_set_name}"
        column_details = []
        for col_name in COMMON_COLUMNS:
            column = Column(
                column_name=col_name,
                column_type="numeric" if col_name == "age" else "string",
                dataset_id=data_set_id,
                meta={}
            )

            session.add(column)
            session.flush()
            column_details.append([column.id, col_name])

        data_set_to_columns[combined_key] = column_details

    return data_set_to_columns