from faker import Faker
from sqlalchemy.orm import Session
from app.models.workspace_model import Workspace
from app.schemas.common_schema import UserRole

fake = Faker()


def create_workspace(session: Session, user_id: str, user_role: UserRole) -> str:
    """
    Generates and inserts random workspace data into the database.

    Args:
        session (Session): SQLAlchemy session object.
        user_id (str): ID of the user who owns the workspace.
        user_role (UserRole): Role of the user.

    Returns:
        str: ID of the created workspace.
    """
    if user_role != UserRole.ADMIN:
        raise ValueError("Only admins can create workspaces.")

    workspace = Workspace(
        name=fake.company(),
        user_id=user_id,
    )

    session.add(workspace)
    session.flush()

    return workspace.id

