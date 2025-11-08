from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.user import User


class UserRepository:
    """Repository for User database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[User]:
        """Get all users."""
        return self.db.query(User).all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def create(self, email: str, username: str) -> User:
        """Create a new user."""
        user = User(email=email, username=username)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
