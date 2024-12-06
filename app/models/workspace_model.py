from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from app.models.base_uuid_model import BaseUUIDModel
from app.models.workspace_user_link_model import WorkspaceUserLink
from uuid import UUID


class WorkSpaceBase(SQLModel):
    name: str = Field(index=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)


class Workspace(BaseUUIDModel, WorkSpaceBase, table=True):
    __tablename__ = "workspace"

    users: list["User"] = Relationship(
        back_populates="workspaces",
        link_model=WorkspaceUserLink,
    )
