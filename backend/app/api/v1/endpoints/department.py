from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.db import get_db_session
from ....models.tables import Department
from ....schemas.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter()

@router.get("/", response_model=List[DepartmentResponse])
def list_departments(
    skip: int = 0,
    limit: int = 100,
    org_id: int = None,
    db: Session = Depends(get_db_session)
):
    """List departments, optionally filtered by organization"""
    query = db.query(Department)
    if org_id:
        query = query.filter(Department.OrganizationID == org_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db_session)
):
    """Create new department"""
    db_dept = Department(**department.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.get("/{dept_id}", response_model=DepartmentResponse)
def get_department(
    dept_id: int,
    db: Session = Depends(get_db_session)
):
    """Get department by ID"""
    db_dept = db.query(Department).filter(Department.DepartmentID == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_dept

@router.put("/{dept_id}", response_model=DepartmentResponse)
def update_department(
    dept_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db_session)
):
    """Update department"""
    db_dept = db.query(Department).filter(Department.DepartmentID == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for field, value in department.model_dump(exclude_unset=True).items():
        setattr(db_dept, field, value)
    
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.delete("/{dept_id}", response_model=DepartmentResponse)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete department"""
    db_dept = db.query(Department).filter(Department.DepartmentID == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_dept)
    db.commit()
    return db_dept 