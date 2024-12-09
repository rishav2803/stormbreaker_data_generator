from faker import Faker
from sqlalchemy.orm import Session
from app.models.column_model import Column
from constants import COMMON_COLUMNS

fake = Faker()

def create_data_set_columns(session: Session, data_set_ids: list[str]) -> dict[str, list[str]]:
    """
    Creates columns for generated data sets and returns a mapping of data_set_id to column_ids.

    Args:
        session (Session): SQLAlchemy session object.
        data_set_ids (list[str]): All the data set IDs created.

    Returns:
        dict[str, list[str]]: A mapping of data_set_id to a list of column IDs.
    """

    data_set_to_columns = {}

    for data_set_id in data_set_ids:
        column_ids = []
        for col_name in COMMON_COLUMNS:
            column = Column(
                column_name=col_name,
                column_type="numeric" if col_name == "age" else "string",
                dataset_id=data_set_id,
                meta={}
            )

            session.add(column)
            session.flush()
            column_ids.append(column.id)

        data_set_to_columns[data_set_id] = column_ids

    return data_set_to_columns

