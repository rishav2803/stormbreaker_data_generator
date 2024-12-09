import argparse
from app.generator.user_generator import create_user
from app.generator.workspace_generator import create_workspace
from app.generator.workspace_link_generator import create_workspace_link
from app.generator.datasource_generator import create_datasource
from app.generator.dataset_generator import create_dataset
from app.generator.dataset_column_generator import create_data_set_columns
from app.generator.validations_generator import create_validation
from app.generator.validation_result_generator import create_validation_result
from app.db.database import SessionLocal
from app.generator.job_generator import create_job


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to populate demo data"
    )
    parser.add_argument(
        "--num_sources",
        type=int,
        default=None,
        help="Number of data sources to create (default: 1)",
    )
    parser.add_argument(
        "--num_sets",
        type=int,
        default=None,
        help="Number of data sets per data source (default: 1)",
    )
    parser.add_argument(
        "--num_validations",
        type=int,
        default=None,
        help="Number of validations to create (default: 1)",
    )

    args = parser.parse_args()

    num_sources = args.num_sources if args.num_sources is not None else int(
        input("Enter the number of data sources: ")
    )
    num_data_sets = args.num_sets if args.num_sets is not None else int(
        input("Enter the number of data sets per data source: ")
    )
    num_validations = args.num_validations if args.num_validations is not None else int(
        input("Enter the number of validations: ")
    )

    print(f"Number of Data Sources: {num_sources}")
    print(f"Number of Data Sets per Data Source: {num_data_sets}")
    print(f"Number of Validations: {num_validations}")

    print("Generating Data for testing...")

    session = SessionLocal()

    try:
        user_id, user_role = create_user(session)

        workspace_id = create_workspace(session, user_id, user_role)

        create_workspace_link(session, user_id, workspace_id)

        data_source_ids = create_datasource(
            session, workspace_id, user_id, num_sources
        )

        dataset_details = create_dataset(
            session, num_data_sets, data_source_ids
        )

        mapped_column_ids = create_data_set_columns(session, dataset_details)

        all_validations = create_validation(
            session, mapped_column_ids, num_validations, user_id
        )

        all_validation_jobs = create_job(
            session, all_tasks=all_validations, type="validation"
        )

        failed_validations = create_validation_result(
            session, all_validation_jobs
        )

        session.commit()
        print("Data Generated Successfully!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}. All changes have been rolled back.")
    finally:
        session.close()


if __name__ == "__main__":
    main()

