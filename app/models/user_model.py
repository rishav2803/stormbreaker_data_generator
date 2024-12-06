from sqlmodel import JSON, Column, Enum, Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from app.models.workspace_user_link_model import WorkspaceUserLink
from app.schemas.common_schema import ProviderType, UserRole, UserStatus


class UserBase(SQLModel):
    name: str = Field(max_length=64, min_length=1, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    provider: ProviderType = Field(sa_column=Column(Enum(ProviderType)))
    role: UserRole = Field(sa_column=Column(Enum(UserRole)))
    status: UserStatus = Field(sa_column=Column(Enum(UserStatus)))
    password: str | None = Field(nullable=True)


class User(BaseUUIDModel, UserBase, table=True):
    __tablename__ = "user"

    validations: list["Validation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"},
    )
    invites: list["Invitation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"},
    )
    workspaces: list["Workspace"] = Relationship(
        back_populates="users",
        link_model=WorkspaceUserLink,
        sa_relationship_kwargs={"lazy": "select"},
    )
    comparisons: list["Comparison"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"},
    )
    data_sources: list["DataSource"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"},
    )
    activities: list["Activity"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"},
    )
