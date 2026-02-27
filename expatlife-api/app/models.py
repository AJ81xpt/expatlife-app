from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .db import Base

class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iso2: Mapped[str] = mapped_column(String(2), unique=True, index=True)
    name_en: Mapped[str] = mapped_column(String(120))
    name_pt: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cities: Mapped[list["City"]] = relationship(back_populates="country", cascade="all, delete-orphan")
    tasks: Mapped[list["Task"]] = relationship(back_populates="country", cascade="all, delete-orphan")

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    lat: Mapped[float] = mapped_column(Numeric(9,6))
    lng: Mapped[float] = mapped_column(Numeric(9,6))
    country: Mapped["Country"] = relationship(back_populates="cities")
    places: Mapped[list["Place"]] = relationship(back_populates="city", cascade="all, delete-orphan")
    costs: Mapped[list["CostOfLiving"]] = relationship(back_populates="city", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    category: Mapped[str] = mapped_column(String(60), index=True)
    title_en: Mapped[str] = mapped_column(String(160))
    title_pt: Mapped[str | None] = mapped_column(String(160), nullable=True)
    summary_en: Mapped[str] = mapped_column(String(280))
    summary_pt: Mapped[str | None] = mapped_column(String(280), nullable=True)
    last_reviewed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    country: Mapped["Country"] = relationship(back_populates="tasks")
    steps: Mapped[list["TaskStep"]] = relationship(back_populates="task", cascade="all, delete-orphan")
    documents: Mapped[list["TaskDocument"]] = relationship(back_populates="task", cascade="all, delete-orphan")
    links: Mapped[list["TaskLink"]] = relationship(back_populates="task", cascade="all, delete-orphan")

class TaskStep(Base):
    __tablename__ = "task_steps"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True)
    step_order: Mapped[int] = mapped_column(Integer)
    title_en: Mapped[str] = mapped_column(String(160))
    title_pt: Mapped[str | None] = mapped_column(String(160), nullable=True)
    body_en: Mapped[str] = mapped_column(Text)
    body_pt: Mapped[str | None] = mapped_column(Text, nullable=True)
    task: Mapped["Task"] = relationship(back_populates="steps")

class TaskDocument(Base):
    __tablename__ = "task_documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True)
    name_en: Mapped[str] = mapped_column(String(160))
    name_pt: Mapped[str | None] = mapped_column(String(160), nullable=True)
    required: Mapped[bool] = mapped_column(Boolean, default=True)
    notes_en: Mapped[str | None] = mapped_column(String(280), nullable=True)
    notes_pt: Mapped[str | None] = mapped_column(String(280), nullable=True)
    task: Mapped["Task"] = relationship(back_populates="documents")

class TaskLink(Base):
    __tablename__ = "task_links"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True)
    label_en: Mapped[str] = mapped_column(String(160))
    label_pt: Mapped[str | None] = mapped_column(String(160), nullable=True)
    url: Mapped[str] = mapped_column(String(500))
    link_type: Mapped[str] = mapped_column(String(30), default="official")
    task: Mapped["Task"] = relationship(back_populates="links")

class Place(Base):
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), index=True)
    place_type: Mapped[str] = mapped_column(String(30), index=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    address: Mapped[str] = mapped_column(String(280))
    lat: Mapped[float] = mapped_column(Numeric(9,6))
    lng: Mapped[float] = mapped_column(Numeric(9,6))
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tags: Mapped[str | None] = mapped_column(String(280), nullable=True)
    city: Mapped["City"] = relationship(back_populates="places")

class CostOfLiving(Base):
    __tablename__ = "cost_of_living"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), index=True)
    rent_1br_min: Mapped[int] = mapped_column(Integer)
    rent_1br_max: Mapped[int] = mapped_column(Integer)
    rent_3br_min: Mapped[int] = mapped_column(Integer)
    rent_3br_max: Mapped[int] = mapped_column(Integer)
    utilities_min: Mapped[int] = mapped_column(Integer)
    utilities_max: Mapped[int] = mapped_column(Integer)
    transport_monthly_min: Mapped[int] = mapped_column(Integer)
    transport_monthly_max: Mapped[int] = mapped_column(Integer)
    groceries_monthly_min: Mapped[int] = mapped_column(Integer)
    groceries_monthly_max: Mapped[int] = mapped_column(Integer)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    city: Mapped["City"] = relationship(back_populates="costs")
