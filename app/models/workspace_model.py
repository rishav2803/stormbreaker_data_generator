from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.models import *
from app.models.base_uuid_model import BaseUUIDModel
from app.models.workspace_user_link_model import WorkspaceUserLink
from uuid import UUID


class WorkSpaceBase(SQLModel):
    name: str = Field(index=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)


class Workspace(BaseUUIDModel, WorkSpaceBase, table=True):
    __tablename__ = "workspace"

    data_sources: list["DataSource"] | None = Relationship(  # noqa: F821
        back_populates="workspace",
        sa_relationship_kwargs={"lazy": "select"},
    )
    users: list["User"] = Relationship(
        back_populates="workspaces",
        link_model=WorkspaceUserLink,
        sa_relationship_kwargs={"lazy": "select"},
    )

    __table_args__ = (
        UniqueConstraint("name", name="unique_workspace_name_constraint"),
    )
