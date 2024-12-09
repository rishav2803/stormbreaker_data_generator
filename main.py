import argparse
from app.generator.user_generator import create_user
from app.generator.workspace_generator import create_workspace
from app.generator.workspace_link_generator import create_workspace_link
from app.generator.datasource_generator import create_datasource
from app.generator.dataset_generator import create_dataset
from app.generator.dataset_column_generator import create_data_set_columns
from app.db.database import SessionLocal


def main():

    num_sources = 1
    num_data_sets = 1
    num_validations = 1
    parser = argparse.ArgumentParser(
        description="CLI tool to configure data sources and data sets.")
    parser.add_argument(
        "--num_sources",
        type=int,
        default=1,
        help="Number of data sources to create (default: 1)",
    )
    parser.add_argument(
        "--num_sets",
        type=int,
        default=1,
        help="Number of data sets per data source (default: 1)",
    )

    parser.add_argument(
        "--num_validations",
        type=int,
        default=1,
        help="Number of Validations (default: 1)",
    )

    args = parser.parse_args()

    if args.num_sources != 1 or args.num_sets != 1:
        num_sources = args.num_sources
        num_data_sets = args.num_sets
        num_validations = args.num_validations
    else:
        num_sources = int(input("Enter the number of data sources: "))

        num_data_sets = int(
            input("Enter the number of data sets per data sources: "))

        num_validations = int(

            input("Enter the number of validations: "))

    print(num_data_sets, num_sources)

    print("Generating Data for testing...")

    session = SessionLocal()

    try:
        user_id, user_role = create_user(session)

        workspace_id = create_workspace(session, user_id, user_role)

        create_workspace_link(session, user_id, workspace_id)

        data_source_ids = create_datasource(
            session, workspace_id, user_id, num_sources)

        dataset_ids = create_dataset(
            session, num_data_sets, data_source_ids)

        # create column
        mapped_column_ids=create_data_set_columns(session,dataset_ids)

        # create validations
        # randomly select a mapped column id and perform validation
        

        session.commit()
        print("Data Generated Sucessfully!!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}. All changes have been rolled back.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
