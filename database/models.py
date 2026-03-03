from sqlalchemy import Column, Float, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Initialize SQLAlchemy Base
Base = declarative_base()


# Mixin to convert SQLAlchemy objects to Python dictionaries
class SerializerMixin:
    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result


# Table for Many-to-Many relationship (Bridge Table)
mission_assignments = Table(
    "mission_assignments",
    Base.metadata,
    Column("astronaut_id", Integer, ForeignKey("astronauts.id"), primary_key=True),
    Column("mission_id", Integer, ForeignKey("missions.id"), primary_key=True),
    Column("role", String, default="Crew Member"),
)


# 1:N Relationship: Agency -> Spacecrafts
class Agency(SerializerMixin, Base):
    __tablename__ = "agencies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)

    # Delete spacecrafts if agency is deleted
    spacecrafts = relationship(
        "Spacecraft", back_populates="agency", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Agency(name='{self.name}', country='{self.country}')>"


# Central table for 1:N and 1:1 relationships
class Spacecraft(SerializerMixin, Base):
    __tablename__ = "spacecrafts"
    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.id"))

    agency = relationship("Agency", back_populates="spacecrafts")

    # 1:1 Relationship: Spacecraft -> BlackBox
    black_box = relationship(
        "BlackBox",
        back_populates="spacecraft",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Spacecraft(model='{self.model_name}')>"


# 1:1 Relationship detail table
class BlackBox(SerializerMixin, Base):
    __tablename__ = "black_boxes"
    id = Column(Integer, primary_key=True)
    serial_number = Column(String, unique=True, nullable=False)
    storage_capacity_gb = Column(Float)

    # unique=True ensures 1:1 relationship
    spacecraft_id = Column(Integer, ForeignKey("spacecrafts.id"), unique=True)
    spacecraft = relationship("Spacecraft", back_populates="black_box")

    def __repr__(self):
        return f"<BlackBox(sn='{self.serial_number}')>"


# N:M Relationship: Astronauts <-> Missions
class Astronaut(SerializerMixin, Base):
    __tablename__ = "astronauts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)

    missions = relationship(
        "Mission", secondary=mission_assignments, back_populates="astronauts"
    )

    def __repr__(self):
        return f"<Astronaut(name='{self.name}', rank='{self.rank}')>"


# N:M Relationship: Missions <-> Astronauts
class Mission(SerializerMixin, Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    destination = Column(String)
    launch_date = Column(DateTime, default=datetime.utcnow)

    astronauts = relationship(
        "Astronaut", secondary=mission_assignments, back_populates="missions"
    )

    def __repr__(self):
        return f"<Mission(title='{self.title}', destination='{self.destination}')>"
