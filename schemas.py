from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    goal: str


class ClientUpdate(BaseModel):
    weight: float | None = Field(default=None, gt=0)
    goal: str | None = None


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
