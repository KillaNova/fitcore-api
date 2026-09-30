from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import (
    ClientCreate,
    ClientSchema,
    ClientUpdate,
    ProgressEntryCreate,
    ProgressEntrySchema,
)
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_client_or_404(client_id: int, db: Session) -> models.Client:
    client = db.get(models.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client niet gevonden")
    return client


@app.post("/clients", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    client = models.Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@app.get("/clients", response_model=list[ClientSchema])
def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Client)
        .order_by(models.Client.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/clients/{client_id}", response_model=ClientSchema)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return get_client_or_404(client_id, db)


@app.put("/clients/{client_id}", response_model=ClientSchema)
def update_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    client = get_client_or_404(client_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = get_client_or_404(client_id, db)
    db.delete(client)
    db.commit()


@app.post(
    "/clients/{client_id}/progress",
    response_model=ProgressEntrySchema,
    status_code=status.HTTP_201_CREATED,
)
def add_progress(
    client_id: int, data: ProgressEntryCreate, db: Session = Depends(get_db)
):
    get_client_or_404(client_id, db)
    entry = models.ProgressEntry(client_id=client_id, **data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/clients/{client_id}/progress", response_model=list[ProgressEntrySchema])
def get_progress(client_id: int, db: Session = Depends(get_db)):
    get_client_or_404(client_id, db)
    return (
        db.query(models.ProgressEntry)
        .filter(models.ProgressEntry.client_id == client_id)
        .order_by(models.ProgressEntry.datum, models.ProgressEntry.id)
        .all()
    )
