from sqlalchemy.orm import Session  
import models, schemas
import bcrypt

def get_movies(db: Session):
    return db.query(models.Movie).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_employees(db: Session):
    return db.query(models.Employee).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Create the employee
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # If the role is 'Manager', add to permissions
    if db_employee.role.lower() == "manager":
        hashed_password = bcrypt.hashpw("Aa123456".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        db_permission = models.Permission(
            username=db_employee.first_name,
            password=hashed_password
        )
        db.add(db_permission)
        db.commit()

    return db_employee

def get_branches(db: Session):
    return db.query(models.Branch).all()

# Replace this function
def create_branch(db: Session, branch: schemas.BranchCreate):
    # Validate that the manager exists and has the "Manager" role
    manager = db.query(models.Employee).filter(
        models.Employee.personal_id == branch.manager_id,
        models.Employee.role == "Manager"
    ).first()
    if not manager:
        raise ValueError("Manager ID must correspond to an existing manager.")
    
    # Create the branch
    db_branch = models.Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

