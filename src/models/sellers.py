from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .books import Book


class Seller(BaseModel):
    __tablename__ = "sellers_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    e_mail: Mapped[str]
    password: Mapped[str]

    books: Mapped[list[Book]] = relationship("Book", back_populates="seller", cascade="all, delete")
