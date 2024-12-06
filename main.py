import argparse
from app.generator.user_generator import create_user
from app.generator.workspace_generator import create_workspace
from app.generator.workspace_link_generator import create_workspace_link
from app.generator.datasource_generator import create_datasource
from app.generator.dataset_generator import create_dataset
from app.db.database import SessionLocal


def main():

    num_sources = 1
    num_data_sets = 1
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

    args = parser.parse_args()

    if args.num_sources != 1 or args.num_sets != 1:
        num_sources = args.num_sources
        num_data_sets = args.num_sets
    else:
        num_sources = int(input("Enter the number of data sources: "))
        num_data_sets = int(
            input("Enter the number of data sets per data sources: "))

    print(num_data_sets, num_sources)

    print("Generating Data for testing...")

    session = SessionLocal()

    try:
        user_id, user_role = create_user(session)
        workspace_id = create_workspace(session, user_id, user_role)
        create_workspace_link(session, user_id, workspace_id)
        for i in range(0,num_sources):
            datasource_id=create_datasource(session,workspace_id,user_id)
            for j in range(0,num_data_sets):
                create_dataset(session,datasource_id)

            
        session.commit()
        print("Data Generated Sucessfully!!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}. All changes have been rolled back.")
    finally:
        session.close()


if __name__ == "__main__":
    main()