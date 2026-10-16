from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, Numeric, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.db.base import Base

class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(24, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    currency: Mapped["Currency"] = relationship("Currency", back_populates="prices", lazy="selectin")

    __table_args__ = (
            UniqueConstraint("currency_id", "timestamp", name="uq_prices_currency_id_timestamp"),
        )