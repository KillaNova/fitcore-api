from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)

    progress = relationship(
        "ProgressEntry", back_populates="client", cascade="all, delete-orphan"
    )


class ProgressEntry(Base):
    __tablename__ = "progress_entries"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    datum = Column(Date, default=date.today)
    gewicht = Column(Float)
    gewicht_verloren = Column(Float)
    vet_percentage = Column(Float)
    vet_verloren = Column(Float)
    skeletal_muscle = Column(Float)
    muscle_mass = Column(Float)

    client = relationship("Client", back_populates="progress")
