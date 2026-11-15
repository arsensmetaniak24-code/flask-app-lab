from datetime import datetime
from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app import db

CATEGORIES = ['news', 'publication', 'tech', 'other']

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    content: Mapped[str] = mapped_column(Text)
    posted: Mapped[datetime] = mapped_column(default=datetime.now)
    category: Mapped[str | None] = mapped_column(Enum(*CATEGORIES, name='category'))

    def __repr__(self) -> str:
        return f"<Post {self.id}: {self.title}>"