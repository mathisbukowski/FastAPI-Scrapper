import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from ..services.user_service import UserService
from ..models.user import User as UserModel


@strawberry.type
class User:
    """GraphQL User type."""
    id: int
    email: str
    username: str
    created_at: datetime
    
    @staticmethod
    def from_model(user: UserModel) -> "User":
        """Convert SQLAlchemy model to GraphQL type."""
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at
        )


@strawberry.type
class Query:
    """GraphQL Query type with available queries."""
    
    @strawberry.field
    def hello(self) -> str:
        """Simple hello world query."""
        return "Plop GraphQL!"

    @strawberry.field
    def db_status(self, info: strawberry.Info) -> str:
        """Check database connection status."""
        db: Session = info.context["db"]
        
        try:
            db.execute(text("SELECT 1"))
            return "Database connection is active."
        except Exception as e:
            return f"Database connection fail: {str(e)}"
    
    @strawberry.field
    def users(self, info: strawberry.Info) -> List[User]:
        """Get all users."""
        db: Session = info.context["db"]
        service = UserService(db)
        users = service.get_all_users()
        return [User.from_model(u) for u in users]
    
    @strawberry.field
    def user(self, info: strawberry.Info, user_id: int) -> Optional[User]:
        """Get user by ID."""
        db: Session = info.context["db"]
        service = UserService(db)
        user = service.get_user_by_id(user_id)
        return User.from_model(user) if user else None


@strawberry.type
class Mutation:
    """GraphQL Mutation type for data modifications."""
    
    @strawberry.field
    def create_user(self, info: strawberry.Info, email: str, username: str) -> User:
        """Create a new user."""
        db: Session = info.context["db"]
        service = UserService(db)
        try:
            user = service.create_user(email=email, username=username)
            return User.from_model(user)
        except ValueError as e:
            raise Exception(str(e))
    
    @strawberry.field
    def delete_user(self, info: strawberry.Info, user_id: int) -> bool:
        """Delete a user by ID."""
        db: Session = info.context["db"]
        service = UserService(db)
        try:
            return service.delete_user(user_id)
        except ValueError as e:
            raise Exception(str(e))

