from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.db import get_db_session
from ....models.tables import PositionJob
from ....schemas.schemas import PositionCreate, PositionUpdate, PositionResponse

router = APIRouter()

@router.get("/", response_model=List[PositionResponse])
def list_positions(
    skip: int = 0,
    limit: int = 100,
    department_id: int = None,
    db: Session = Depends(get_db_session)
):
    """List positions, optionally filtered by department"""
    query = db.query(PositionJob)
    if department_id:
        query = query.filter(PositionJob.DepartmentID == department_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=PositionResponse)
def create_position(
    position: PositionCreate,
    db: Session = Depends(get_db_session)
):
    """Create new position"""
    db_position = PositionJob(**position.model_dump())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@router.get("/{position_id}", response_model=PositionResponse)
def get_position(
    position_id: int,
    db: Session = Depends(get_db_session)
):
    """Get position by ID"""
    db_position = db.query(PositionJob).filter(PositionJob.PositionID == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@router.put("/{position_id}", response_model=PositionResponse)
def update_position(
    position_id: int,
    position: PositionUpdate,
    db: Session = Depends(get_db_session)
):
    """Update position"""
    db_position = db.query(PositionJob).filter(PositionJob.PositionID == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    for field, value in position.model_dump(exclude_unset=True).items():
        setattr(db_position, field, value)
    
    db.commit()
    db.refresh(db_position)
    return db_position

@router.delete("/{position_id}", response_model=PositionResponse)
def delete_position(
    position_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete position"""
    db_position = db.query(PositionJob).filter(PositionJob.PositionID == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    db.delete(db_position)
    db.commit()
    return db_position 