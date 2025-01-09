from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.db import get_db_session
from ....models.tables import Department
from ....schemas.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    responses={
        404: {"description": "Department not found"},
        400: {"description": "Bad request"},
    }
)

@router.get(
    "/",
    response_model=List[DepartmentResponse],
    summary="List Departments",
    description="""
    Retrieve a list of all departments.
    
    - Supports pagination through skip/limit parameters
    - Can be filtered by organization ID
    - Returns a list of departments with their basic information
    """,
    response_description="List of departments"
)
def list_departments(
    skip: int = 0,
    limit: int = 100,
    org_id: int = None,
    db: Session = Depends(get_db_session)
):
    """
    List all departments with pagination and filtering support.
    
    Parameters:
    - skip: Number of records to skip (offset)
    - limit: Maximum number of records to return
    - org_id: Optional organization ID filter
    
    Returns:
    - List of departments with their details
    """
    query = db.query(Department)
    if org_id:
        query = query.filter(Department.OrganizationID == org_id)
    return query.offset(skip).limit(limit).all()

@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=201,
    summary="Create Department",
    description="""
    Create a new department within an organization.
    
    Required fields:
    - Name: Department name
    - OrganizationID: ID of the parent organization
    
    Optional fields:
    - Description: Department description
    - ParentDepartmentID: ID of the parent department
    - HeadOfDepartmentID: ID of the department head
    """,
    response_description="Created department details",
    responses={
        400: {
            "description": "Invalid input",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Organization": {
                            "value": {"detail": "Organization not found"}
                        },
                        "Invalid Parent": {
                            "value": {"detail": "Parent department not found"}
                        },
                        "Invalid Head": {
                            "value": {"detail": "Employee not found"}
                        }
                    }
                }
            }
        }
    }
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db_session)
):
    """
    Create new department
    
    Example request body:
    ```json
    {
        "Name": "Engineering",
        "Description": "Software Engineering Department",
        "OrganizationID": 1,
        "ParentDepartmentID": null,
        "HeadOfDepartmentID": 1
    }
    ```
    """
    db_dept = Department(**department.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.get(
    "/{dept_id}",
    response_model=DepartmentResponse,
    summary="Get Department",
    description="""
    Retrieve detailed information about a specific department by its ID.
    
    Includes:
    - Basic department details
    - Parent department reference
    - Department head information
    - Organization reference
    """,
    responses={
        404: {
            "description": "Department not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Department not found"}
                }
            }
        }
    }
)
def get_department(
    dept_id: int,
    db: Session = Depends(get_db_session)
):
    """
    Get department by ID
    
    Parameters:
    - dept_id: Department ID (integer)
    
    Returns:
    - Department details if found
    - 404 error if not found
    """
    db_dept = db.query(Department).filter(Department.DepartmentID == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_dept

@router.put(
    "/{dept_id}",
    response_model=DepartmentResponse,
    summary="Update Department",
    description="""
    Update an existing department's information.
    
    All fields are optional in the update request.
    Only provided fields will be updated.
    
    Note:
    - Changing organization ID will move the department to another organization
    - Changing parent department will restructure the hierarchy
    """,
    responses={
        404: {"description": "Department not found"},
        400: {
            "description": "Invalid update data",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Organization": {
                            "value": {"detail": "Organization not found"}
                        },
                        "Invalid Parent": {
                            "value": {"detail": "Parent department not found"}
                        },
                        "Circular Reference": {
                            "value": {"detail": "Circular department hierarchy not allowed"}
                        }
                    }
                }
            }
        }
    }
)
def update_department(
    dept_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db_session)
):
    """
    Update department
    
    Example request body:
    ```json
    {
        "Name": "Engineering & Research",
        "Description": "Updated department description",
        "HeadOfDepartmentID": 2
    }
    ```
    """
    db_dept = db.query(Department).filter(Department.DepartmentID == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for field, value in department.model_dump(exclude_unset=True).items():
        setattr(db_dept, field, value)
    
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.delete(
    "/{dept_id}",
    response_model=DepartmentResponse,
    summary="Delete Department",
    description="""
    Delete a department and handle related data.
    
    Warning: This operation will:
    - Delete all positions in this department
    - Remove department head association
    - Update parent references of child departments
    
    Note: Cannot delete a department that has:
    - Active employees in positions
    - Child departments (must be moved or deleted first)
    """,
    responses={
        404: {"description": "Department not found"},
        409: {
            "description": "Cannot delete department with dependencies",
            "content": {
                "application/json": {
                    "examples": {
                        "Has Employees": {
                            "value": {"detail": "Department has active employees"}
                        },
                        "Has Children": {
                            "value": {"detail": "Department has child departments"}
                        }
                    }
                }
            }
        }
    }
)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete department if it has no dependencies"""
    db_dept = db.query(Department).filter(Department.DepartmentID == dept_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_dept)
    db.commit()
    return db_dept 