from typing import Optional
from typing import List
from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Bike(Base):
    __tablename__ = "bikes"
    id: Mapped[int] = mapped_column(primary_key = True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    battery: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    station_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    rentals: Mapped[List["Rental"]] = relationship(
        "Rental",
        back_populates="bike"
    )

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    rentals: Mapped[List["Rental"]] = relationship(
        "Rental",
        back_populates="user"
    )

class Rental(Base):
    __tablename__ = "rentals"
    id: Mapped[int] = mapped_column(primary_key=True)
    bike_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bikes.id", ondelete= "SET NULL"),
        nullable = True
    )

    user_id: Mapped[Optional[int]] = mapped_column(Float, nullable=False)

    bike: Mapped[Optional["Bike"]] = relationship(
        "Bike",
        back_populates="rentals"
    )

    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="rentals"
    )