from datetime import date

from pydantic import BaseModel, ConfigDict, Field


# EXPANSION: replace the free-text `goal` with an Enum (e.g. "cut", "bulk",
# "maintain", "recomp") so goals can be filtered and used in calculations.


class ClientCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    goal: str


class ClientUpdate(BaseModel):
    weight: float | None = Field(default=None, gt=0)
    goal: str | None = None

    # EXPANSION: allow updating name and age too (e.g. to fix a typo or
    # after a birthday). Add them here as optional fields.


class ClientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    weight: float
    goal: str


class ProgressEntryCreate(BaseModel):
    gewicht: float = Field(gt=0)
    gewicht_verloren: float
    vet_percentage: float = Field(ge=0, le=100)
    vet_verloren: float
    skeletal_muscle: float = Field(ge=0)
    muscle_mass: float = Field(ge=0)

    # EXPANSION: optional `datum: date | None = None` so old measurements
    # can be entered with their real date (now it is always today).


class ProgressEntrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    datum: date
    gewicht: float
    gewicht_verloren: float
    vet_percentage: float
    vet_verloren: float
    skeletal_muscle: float
    muscle_mass: float


# EXPANSION: ProgressSummarySchema for a summary endpoint: start weight,
# current weight, total kg lost, total fat % lost, weeks in program.
