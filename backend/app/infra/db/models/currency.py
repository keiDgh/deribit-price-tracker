from app.infra.db.base import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    prices: Mapped[list["Price"]] = relationship(back_populates="currency", lazy="selectin")