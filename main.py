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

# EXPANSION: database migrations. create_all only creates missing tables; it
# never changes existing ones. Switch to Alembic so new columns/indexes
# (see the EXPANSION notes in models.py) reach your existing database.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# EXPANSION: CORS. When a frontend (website/app) calls this API from another
# domain, add CORSMiddleware here with the allowed origins.

# EXPANSION: split into routers once this file grows: routers/clients.py,
# routers/progress.py, routers/workouts.py, then app.include_router(...).


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# EXPANSION: authentication. Add a get_current_coach dependency (JWT login
# via OAuth2PasswordBearer) and require it on every endpoint below, so the
# API is not open to anyone who knows the URL.


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
    # EXPANSION: search and filters, e.g. ?name=eren (ILIKE search) and
    # ?goal=cut, plus ?sort=name to choose the order.
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
    # exclude_none: an explicit null would otherwise wipe the column and make
    # this client fail response validation on every later read.
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    # EXPANSION: soft delete. Set client.is_active = False instead of deleting,
    # so progress history is kept and a client can be restored later.
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
    client = get_client_or_404(client_id, db)
    # EXPANSION: auto-calculate gewicht_verloren and vet_verloren by comparing
    # with the client's first entry, instead of typing them in by hand.
    # EXPANSION: also set client.weight = data.gewicht, so the client's weight
    # always matches their latest check-in.
    entry = models.ProgressEntry(client_id=client.id, **data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/clients/{client_id}/progress", response_model=list[ProgressEntrySchema])
def get_progress(client_id: int, db: Session = Depends(get_db)):
    get_client_or_404(client_id, db)
    # EXPANSION: date range filter (?from=2026-01-01&to=2026-03-31) and
    # pagination for clients with a long history.
    return (
        db.query(models.ProgressEntry)
        .filter(models.ProgressEntry.client_id == client_id)
        .order_by(models.ProgressEntry.datum, models.ProgressEntry.id)
        .all()
    )


# EXPANSION: GET /clients/{client_id}/progress/summary. Returns start vs
# current weight, total kg and fat % lost and weekly average (see
# ProgressSummarySchema in schemas.py). Useful for client reports.

# EXPANSION: PUT/DELETE /clients/{client_id}/progress/{entry_id} to correct
# or remove a wrong measurement.

# EXPANSION: workout endpoints (POST/GET /clients/{client_id}/workouts) once
# the Workout model in models.py exists.

# EXPANSION: nutrition endpoints (POST/GET /clients/{client_id}/nutrition)
# once the NutritionPlan model in models.py exists.

# EXPANSION: export endpoint (GET /clients/{client_id}/export) that returns
# the progress history as CSV or PDF to send to the client.
