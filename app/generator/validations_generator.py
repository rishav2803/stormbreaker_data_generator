from faker import Faker
from sqlalchemy.orm import Session
from app.models.validation_model import Validation
from constants import COMMON_COLUMNS
import random
from constants import VALIDATIONS

fake = Faker()


def build_validation_name(dataset_name: str, selected_column_name: str, selected_validation) -> str:
    return f"{dataset_name} {selected_column_name} {selected_validation}"


def build_configuration(dataset_name: str, selected_column_name: str, selected_validation):
    validation_name = build_validation_name(
        dataset_name, selected_column_name, selected_validation)
    return {
        "definition": {
            validation_name: {
                "on": f"{validation_name}({selected_column_name})",
                "threshold": "auto",
                "where": "",
                "values": [],
                "regex": None
            }
        },
        "presentation": {
            "name": f"{validation_name}({selected_column_name})",
            "column": f"{selected_column_name}",
            "function": f"{selected_validation}",
            "filters": [],
            "threshold": "auto",
            "query": None,
            "regex": None,
            "values": None
        }
    }


def create_validation(session: Session, mapped_column_ids: dict[str, list[list[str]]], num_validations: int, user_id: str) -> list[str]:
    """
    Create Validations.

    Args:
        session (Session): SQLAlchemy session object.
        mapped_column_ids (dict[str,list[str]]): Dict storing the mapping of multiple data sets and their columns.
        num_validations (int): Number of validations to perform.
        user_id(str) : User id


    Returns:
        list[str]: List of validations ID's.
    """

    validation_list = random.sample(range(0, 4), num_validations)
    validation_runs = 1
    all_validations = []

    for i in range(0, validation_runs):
        selected_dataset_details = random.choice(
            list(mapped_column_ids.keys()))

        dataset_id, dataset_name = selected_dataset_details.split('/')

        selected_column_id, selected_column_name = random.choice(
            mapped_column_ids[selected_dataset_details])

        selected_validation = VALIDATIONS[random.choice(validation_list)]
        configuration = build_configuration(
            dataset_name, selected_column_name, selected_validation)
        validation_name = build_validation_name(
            dataset_name, selected_column_name, selected_validation)
        validation = Validation(
            name=validation_name,
            configuration=configuration,
            type=selected_validation,
            is_auto=True,
            auto_status="IN_REVIEW",
            category="DISTRIBUTIONS",
            dataset_id=dataset_id,
            column_id=selected_column_id,
            user_id=user_id,
        )

        session.add(validation)
        session.flush()
        all_validations.append(validation.id)

    return all_validations
