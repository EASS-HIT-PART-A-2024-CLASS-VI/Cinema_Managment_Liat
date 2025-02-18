from sqlalchemy.orm import Session
import models, schemas
import bcrypt

def get_movies(db: Session):
    return db.query(models.Movie).all()

def get_movie_by_name(db: Session, movie_name: str):
    return db.query(models.Movie).filter(models.Movie.title == movie_name).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie_by_id(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        return {"error": "Movie not found"}
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}

def get_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee_by_name(db: Session, employee_name: str):
    return db.query(models.Employee).filter(models.Employee.first_name + " " + models.Employee.last_name == employee_name).all()

def get_sorted_employees_by_salary(db: Session):
    return db.query(models.Employee).order_by(models.Employee.salary.desc()).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    if db_employee.role.lower() == "manager":
        hashed_password = bcrypt.hashpw("Aa123456".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        db_permission = models.Permission(
            username=db_employee.first_name,
            password=hashed_password
        )
        db.add(db_permission)
        db.commit()

    return db_employee

def delete_employee_by_id(db: Session, employee_id: int):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        return {"error": "Employee not found"}

    if employee.role.lower() == "manager":
        permission = db.query(models.Permission).filter(
            models.Permission.username == employee.first_name
        ).first()
        if permission:
            db.delete(permission)

    db.delete(employee)
    db.commit()
    return {
        "message": "Employee and associated permissions deleted successfully"
        if employee.role.lower() == "manager"
        else "Employee deleted successfully"
    }

def get_branches(db: Session):
    return db.query(models.Branch).all()

def get_branch_by_name(db: Session, branch_name: str):
    return db.query(models.Branch).filter(models.Branch.name == branch_name).all()

def create_branch(db: Session, branch: schemas.BranchCreate):
    manager = db.query(models.Employee).filter(
        models.Employee.personal_id == branch.manager_id,
        models.Employee.role == "Manager"
    ).first()
    if not manager:
        raise ValueError("Manager ID must correspond to an existing manager.")
    
    db_branch = models.Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def delete_branch_by_id(db: Session, branch_id: int):
    branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not branch:
        return {"error": "Branch not found"}
    db.delete(branch)
    db.commit()
    return {"message": "Branch deleted successfully"}
