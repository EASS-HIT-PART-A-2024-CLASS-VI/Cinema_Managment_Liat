from fastapi import FastAPI, Depends, HTTPException
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
    return {"message": "Welcome to the Cinema Management System!"}

# Movies endpoints
@app.get("/movies", response_model=list[schemas.Movie])
def read_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/movies/dropdown", response_model=list[str])
def get_movie_titles(db: Session = Depends(get_db)):
    return [movie.title for movie in crud.get_movies(db)]

@app.post("/movies", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, movie)

# Employees endpoints
@app.get("/employees", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.get("/employees/dropdown", response_model=list[str])
def get_employee_ids(db: Session = Depends(get_db)):
    return [employee.personal_id for employee in crud.get_employees(db)]

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def get_employee_by_id(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.personal_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/employees", response_model=schemas.Employee)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

# Branches endpoints
@app.get("/branches", response_model=list[schemas.Branch])
def read_branches(db: Session = Depends(get_db)):
    return crud.get_branches(db)

@app.get("/branches/dropdown", response_model=list[str])
def get_branch_names(db: Session = Depends(get_db)):
    return [branch.name for branch in crud.get_branches(db)]

@app.get("/branches/{branch_id}", response_model=schemas.Branch)
def get_branch_by_id(branch_id: int, db: Session = Depends(get_db)):
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

@app.post("/branches", response_model=schemas.Branch)
def add_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    return crud.create_branch(db, branch)

