from sqlalchemy.orm import Session
from app.models.workspace_user_link_model import WorkspaceUserLink


def create_workspace_link(session: Session, user_id: str, workspace_id: str):
    """
    Create's the workspace link.

    Args:
        session (Session): SQLAlchemy session object.
        user_id (str): ID of the user who owns the workspace.
        workspace_id (str): ID of the workspace.
    """

    workspace_link = WorkspaceUserLink(
        user_id=user_id,
        workspace_id=workspace_id
    )

    session.add(workspace_link)
    session.flush()
