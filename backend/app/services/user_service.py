import logging
from typing import List, Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import DatabaseError, UserNotFoundError, UserAlreadyExistsError

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user from the database by their ID.
        """
        try:
            return self.db.get(User, user_id)
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching user with ID {user_id}: {e}", exc_info=True)
            raise DatabaseError("Error fetching user from the database.")

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email, normalizing it to lowercase.
        """
        normalized_email = email.strip().lower()
        try:
            return self.db.query(User).filter(User.email == normalized_email).first()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching user with email {email}: {e}", exc_info=True)
            raise DatabaseError("Error fetching user from the database.")

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lists users with pagination.
        """
        try:
            return self.db.query(User).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error listing users: {e}", exc_info=True)
            raise DatabaseError("Error listing users from the database.")

    def create_user(self, user_in: UserCreate) -> User:
        """
        Creates a new user. Expects a UserCreate object with the password already hashed.
        """
        existing_user = self.get_user_by_email(user_in.email)
        if existing_user:
            raise UserAlreadyExistsError("Email is already registered")
        
        new_user = User(
            email=user_in.email.strip().lower(),
            hashed_password=user_in.password
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            logger.info("User created: %s", new_user.email)
            return new_user
        except IntegrityError as e:
            self.db.rollback()
            logger.error("Integrity error creating user %s: %s", new_user.email, e)
            raise UserAlreadyExistsError("Email is already registered")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Database error creating user %s: %s", new_user.email, e)
            raise DatabaseError("Error creating user.")

    def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        """
        Updates an existing user's fields.
        Expects a UserUpdate object with the password already hashed if it's included.
        """
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise UserNotFoundError("User not found.")

        updates = user_in.dict(exclude_unset=True)

        if "password" in updates:
            updates["hashed_password"] = updates.pop("password")

        if "email" in updates:
            updates["email"] = updates["email"].strip().lower()

        for field, value in updates.items():
            setattr(db_user, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_user)
            logger.info("User updated: %s", db_user.id)
            return db_user
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Database error updating user %s: %s", db_user.id, e)
            raise DatabaseError("Error updating user.")

    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user from the database.
        """
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise UserNotFoundError("User not found.")

        try:
            self.db.delete(db_user)
            self.db.commit()
            logger.info("User deleted: %s", db_user.id)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Database error deleting user %s: %s", db_user.id, e)
            raise DatabaseError("Error deleting user.")