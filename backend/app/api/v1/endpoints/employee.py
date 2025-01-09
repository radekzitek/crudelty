from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.db import get_db_session
from ....models.tables import Employee
from ....schemas.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter()

@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    org_id: int = None,
    db: Session = Depends(get_db_session)
):
    """List employees, optionally filtered by organization"""
    query = db.query(Employee)
    if org_id:
        query = query.filter(Employee.OrganizationID == org_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db_session)
):
    """Create new employee"""
    # Check if email already exists
    if db.query(Employee).filter(Employee.Email == employee.Email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db_session)
):
    """Get employee by ID"""
    db_employee = db.query(Employee).filter(Employee.EmployeeID == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db_session)
):
    """Update employee"""
    db_employee = db.query(Employee).filter(Employee.EmployeeID == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check email uniqueness if being updated
    if employee.Email and employee.Email != db_employee.Email:
        if db.query(Employee).filter(Employee.Email == employee.Email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for field, value in employee.model_dump(exclude_unset=True).items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}", response_model=EmployeeResponse)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete employee"""
    db_employee = db.query(Employee).filter(Employee.EmployeeID == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return db_employee 