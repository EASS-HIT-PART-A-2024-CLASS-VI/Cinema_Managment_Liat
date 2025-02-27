from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel
import bcrypt
import crud, models, schemas, database
import httpx
from typing import List, Optional
from httpx import AsyncClient
from pydantic import BaseModel
from typing import Optional
import logging

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
logger = logging.getLogger(__name__)

# Internal URL for LLM service (using Docker service name)
LLM_SERVICE_URL = "http://llm_service:8001"  # Internal Docker network port

# HTTP client for async requests
llm_client = AsyncClient(base_url=LLM_SERVICE_URL)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cinema Management System!"}

# LLM Service Integration
# Simplified request models

class LLMChatRequest(BaseModel):
    prompt: str
    context: Optional[str] = None

@app.post("/api/llm/chat")
async def forward_to_llm(request: LLMChatRequest):
    """
    Forward chat requests to LLM service
    """
    logger.info(f"Forwarding chat request to LLM service: {request.prompt}")
    try:
        response = await llm_client.post(
            "/chat", 
            json=request.dict()
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error communicating with LLM service: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to process LLM request"
        )

# Login endpoint
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Fetch the user credentials from the permissions table
    result = db.execute(
        text("SELECT password FROM permissions WHERE username = :username"),
        {"username": request.username}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Extract hashed password from result
    hashed_password = result[0]

    # Verify password
    if not bcrypt.checkpw(request.password.encode("utf-8"), hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Successfully logged in as {request.username}"}

@app.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

# Movies endpoints
@app.get("/movies/dropdown", response_model=list[str])
def get_movie_titles(db: Session = Depends(get_db)):
    return [movie.title for movie in crud.get_movies(db)]

@app.get("/movies/sorted", response_model=list[schemas.Movie])
def get_sorted_movies(db: Session = Depends(get_db)):
    """
    Get movies sorted by critics_rating in descending order.
    """
    movies = db.query(models.Movie).order_by(models.Movie.critics_rating.desc()).all()
    return movies

@app.get("/movies", response_model=list[schemas.Movie])
def read_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    """
    Get a movie by its ID.
    """
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/movies", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Add a new movie to the database.
    """
    return crud.create_movie(db, movie)

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie by its ID and return its title to update the screening schedule.
    """
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_title = movie.title
    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted successfully", "deleted_movie": movie_title}

# Employees endpoints
@app.get("/employees", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.get("/employees/dropdown", response_model=list[str])
def get_employee_names(db: Session = Depends(get_db)):
    return [employee.first_name + " " + employee.last_name for employee in crud.get_employees(db)]

@app.get("/employees/sorted", response_model=list[schemas.Employee])
def get_sorted_employees(db: Session = Depends(get_db)):
    """
    Get employees sorted by salary in descending order.
    """
    return crud.get_sorted_employees_by_salary(db)

@app.get("/employees/birthdays")
def get_employees_with_birthdays(db: Session = Depends(get_db)):
    return crud.get_employees_with_birthdays(db)

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def get_employee_by_id(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.personal_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/employees", response_model=schemas.Employee)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = crud.create_employee(db, employee)

    if employee.role.lower() == "manager":
        existing_permission = db.query(models.Permission).filter(
            models.Permission.username == employee.first_name
        ).first()
        if not existing_permission:
            hashed_password = bcrypt.hashpw("Aa123456".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            db_permission = models.Permission(
                username=employee.first_name,
                password=hashed_password
            )
            db.add(db_permission)
            db.commit()

    return new_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    result = crud.delete_employee_by_id(db, employee_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

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

@app.delete("/branches/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    result = crud.delete_branch_by_id(db, branch_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.on_event("shutdown")
async def shutdown_event():
    await llm_client.aclose()