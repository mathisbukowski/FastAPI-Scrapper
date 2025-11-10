from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.item import Item


class ItemRepository:
    """Repository for Item database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(Item.id == item_id).first()

    def list_by_user(self, user_id: int) -> List[Item]:
        return (
            self.db.query(Item)
            .filter(Item.user_id == user_id)
            .order_by(Item.created_at.desc())
            .all()
        )

    def create(self, name: str, user_id: int) -> Item:
        item = Item(name=name, user_id=user_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> bool:
        item = self.get_by_id(item_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
