from typing import List, Optional
from sqlalchemy.orm import Session

from ..repositories.item_repo import ItemRepository
from ..repositories.user_repo import UserRepository
from ..models.item import Item


class ItemService:
    """Service layer for item business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.items = ItemRepository(db)
        self.users = UserRepository(db)

    def create_item_for_user(self, user_id: int, name: str) -> Item:
        user = self.users.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return self.items.create(name=name, user_id=user_id)

    def get_user_items(self, user_id: int) -> List[Item]:
        if not self.users.get_by_id(user_id):
            raise ValueError(f"User with ID {user_id} not found")
        return self.items.list_by_user(user_id)

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        return self.items.get_by_id(item_id)

    def delete_item(self, item_id: int) -> bool:
        if not self.items.get_by_id(item_id):
            raise ValueError(f"Item with ID {item_id} not found")
        return self.items.delete(item_id)
