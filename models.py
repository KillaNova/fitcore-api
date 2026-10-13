from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


# EXPANSION: Coach model. Add a `coaches` table (id, name, email,
# password_hash) and a `coach_id` foreign key on Client, so every coach
# only sees their own clients after logging in.


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)

    # EXPANSION: extra client fields:
    # - email / phone: to contact the client or send progress reports
    # - height + gender: needed to calculate BMI and BMR/calorie needs
    # - created_at: start date, to show "progress since start"
    # - is_active: archive clients instead of deleting them (soft delete)

    progress = relationship(
        "ProgressEntry", back_populates="client", cascade="all, delete-orphan"
    )

    # EXPANSION: relationships for new modules, e.g.
    # workouts = relationship("Workout", back_populates="client")
    # nutrition_plans = relationship("NutritionPlan", back_populates="client")


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

    # EXPANSION: extra measurements per check-in:
    # - waist / hips / chest / arms in cm (tape measurements)
    # - notes: free text from coach or client ("slept badly", "new PR")
    # - photo_url: link to a progress photo

    client = relationship("Client", back_populates="progress")


# EXPANSION: Workout model. Table `workouts` (client_id, datum, exercise,
# sets, reps, weight_kg) to log training sessions and track strength
# progress (e.g. estimated 1RM per exercise over time).

# EXPANSION: NutritionPlan model. Table `nutrition_plans` (client_id,
# calories, protein_g, carbs_g, fat_g, start_date) so the coach can assign
# macro targets per client.
