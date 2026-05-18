from pydantic import BaseModel
from datetime import date

class ClientSchema(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    goal: str

class ProgressEntrySchema(BaseModel):
    id: int
    client_id: int
    datum: date
    gewicht: float
    gewicht_verloren: float
    vet_percentage: float
    vet_verloren: float
    skeletal_muscle: float
    muscle_mass: float

class Config:
    from_attributes = True