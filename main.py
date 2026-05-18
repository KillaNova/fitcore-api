from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import ClientSchema, ProgressEntrySchema
from typing import List
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/clients", response_model=ClientSchema)
def create_client(
    name: str, age: int, weight: float, goal: str, db: Session = Depends(get_db)
):
    client = models.Client(name=name, age=age, weight=weight, goal=goal)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@app.get("/clients", response_model=List[ClientSchema])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client)


@app.put("/clients/{client_id}")
def update_client(
    client_id: int, weight: float, goal: str, db: Session = Depends(get_db)
):
    client = db.query(models.client).filter(models.client.id == client_id).first()
    if not client:
        return {"error": "Client niet gevonden"}
    client.weight = weight
    client.goal = goal
    db.commit()
    return client


@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        return {"error": "Client niet gevonden"}
    db.delete(client)
    db.commit()
    return


@app.post("/clients/{client_id}/progress", response_model=ProgressEntrySchema)
def add_progress(
    client_id: int,
    gewicht: float,
    gewicht_verloren: float,
    vet_percentage: float,
    vet_verloren: float,
    skeletal_muscle: float,
    muscle_mass: float,
    db: Session = Depends(get_db),
):
    entry = models.ProgressEntry(
        client_id=client_id,
        gewicht=gewicht,
        gewicht_verloren=gewicht_verloren,
        vet_percentage=vet_percentage,
        vet_verloren=vet_verloren,
        skeletal_muscle=skeletal_muscle,
        muscle_mass=muscle_mass,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/clients/{client_id}/progress", response_model=List[ProgressEntrySchema])
def get_progress(client_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.ProgressEntry)
        .filter(models.ProgressEntry.client_id == client_id)
        .all()
    )
