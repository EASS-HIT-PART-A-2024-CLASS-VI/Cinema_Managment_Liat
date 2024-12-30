from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "branches": "/branches",
        "employees": "/employees",
        "movies": "/movies"
    }

@app.get("/branches", response_model=list[schemas.Branch])
def read_branches(db: Session = Depends(get_db)):
    return crud.get_branches(db)

@app.post("/branches", response_model=schemas.Branch)
def add_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    return crud.create_branch(db, branch)

@app.get("/employees", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.post("/employees", response_model=schemas.Employee)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.get("/movies", response_model=list[schemas.Movie])
def read_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)

@app.post("/movies", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, movie)
