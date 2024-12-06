
from faker import Faker
from sqlalchemy.orm import Session
# from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.common_schema import ProviderType, UserRole, UserStatus
from typing import Tuple

fake = Faker()


def create_user(session: Session) -> Tuple[str, UserRole]:
    """
    Generates and inserts random user data into the database.

    Args:
        session (Session): SQLAlchemy session object.
        num_users (int): Number of users to create.
    """
    user = User(
        name=fake.name(),
        email=fake.unique.email(),
        provider=ProviderType.EMAIL,
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        password=fake.password(length=12),
    )
    session.add(user)

    return user.id, user.role
