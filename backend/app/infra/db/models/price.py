from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.db.base import Base

class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(24, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)  # UNIX timestamp

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    currency: Mapped["Currency"] = relationship(back_populates="prices", lazy="selectin")

    __table_args__ = (
        Index("ix_prices_ticker_timestamp", "ticker", "timestamp"),
    )