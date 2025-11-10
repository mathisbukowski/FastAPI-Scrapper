from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..core.database import Base
from sqlalchemy.orm import relationship


class Item(Base):
    """Item SQLAlchemy model.

    Represents an item owned by a user. The foreign key enforces the
    relationship and combined with the back_populates on User.items gives us
    bidirectional navigation. Cascade delete on the User side will remove
    orphan items.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    user = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', user_id={self.user_id})>"
