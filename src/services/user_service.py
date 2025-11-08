from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.user_repo import UserRepository
from ..models.user import User


class UserService:
    """Service layer for user business logic."""
    
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self.repo.get_all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.repo.get_by_id(user_id)
    
    def create_user(self, email: str, username: str) -> User:
        """
        Create a new user.
        Validates that email and username are unique.
        """
        # Check if email already exists
        if self.repo.get_by_email(email):
            raise ValueError(f"Email '{email}' already exists")
        
        # Check if username already exists
        if self.repo.get_by_username(username):
            raise ValueError(f"Username '{username}' already exists")
        
        return self.repo.create(email=email, username=username)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        if not self.repo.get_by_id(user_id):
            raise ValueError(f"User with ID {user_id} not found")
        return self.repo.delete(user_id)
