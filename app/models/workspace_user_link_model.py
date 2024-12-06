from uuid import UUID
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class WorkspaceUserLink(SQLModel, table=True):
    __tablename__ = "workspace_user_link"
    workspace_id: UUID = Field(foreign_key="workspace.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
