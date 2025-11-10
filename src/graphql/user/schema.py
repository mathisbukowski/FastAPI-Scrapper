import strawberry
from typing import List, cast
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from ...services.user_service import UserService
from ...services.item_service import ItemService
from ...models.user import User as UserModel
from ...models.item import Item as ItemModel


@strawberry.type
class Item:
    """GraphQL Item type."""
    id: int
    name: str
    created_at: datetime
    user_id: int

    @staticmethod
    def from_model(item: ItemModel) -> "Item":
        return Item(
            id=cast(int, item.id),
            name=cast(str, item.name),
            created_at=cast(datetime, item.created_at),
            user_id=cast(int, item.user_id),
        )


@strawberry.type
class User:
    """GraphQL User type."""
    id: int
    email: str
    username: str
    created_at: datetime

    @strawberry.field
    def items(self, info: strawberry.Info) -> List[Item]:
        """All items owned by this user (lazy-loaded)."""
        db: Session = info.context["db"]
        service = ItemService(db)
        try:
            user_items = service.get_user_items(self.id)
        except ValueError:
            return []
        return [Item.from_model(i) for i in user_items]

    @staticmethod
    def from_model(user: UserModel) -> "User":
        """Convert SQLAlchemy model to GraphQL type."""
        return User(
            id=cast(int, user.id),
            email=cast(str, user.email),
            username=cast(str, user.username),
            created_at=cast(datetime, user.created_at),
        )


@strawberry.type
class UserQuery:
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
    def user(self, info: strawberry.Info, user_id: int) -> User | None:
        """Get user by ID."""
        db: Session = info.context["db"]
        service = UserService(db)
        user = service.get_user_by_id(user_id)
        return User.from_model(user) if user else None

    # Item related queries
    @strawberry.field
    def items(self, info: strawberry.Info, user_id: int) -> List[Item]:
        """List items for a given user."""
        db: Session = info.context["db"]
        service = ItemService(db)
        try:
            items = service.get_user_items(user_id)
        except ValueError as e:
            raise Exception(str(e))
        return [Item.from_model(i) for i in items]


@strawberry.type
class UserMutation:
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

    # Item mutations
    @strawberry.field
    def create_item(self, info: strawberry.Info, user_id: int, name: str) -> Item:
        """Create a new item for a user."""
        db: Session = info.context["db"]
        service = ItemService(db)
        try:
            item = service.create_item_for_user(user_id=user_id, name=name)
            return Item.from_model(item)
        except ValueError as e:
            raise Exception(str(e))

    @strawberry.field
    def delete_item(self, info: strawberry.Info, item_id: int) -> bool:
        """Delete an item by ID."""
        db: Session = info.context["db"]
        service = ItemService(db)
        try:
            return service.delete_item(item_id)
        except ValueError as e:
            raise Exception(str(e))
