from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.db import get_db_session
from ....models.tables import Team, TeamMember
from ....schemas.schemas import TeamCreate, TeamUpdate, TeamResponse, TeamMemberBase

router = APIRouter()

@router.get("/", response_model=List[TeamResponse])
def list_teams(
    skip: int = 0,
    limit: int = 100,
    org_id: int = None,
    db: Session = Depends(get_db_session)
):
    """List teams, optionally filtered by organization"""
    query = db.query(Team)
    if org_id:
        query = query.filter(Team.OrganizationID == org_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=TeamResponse)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db_session)
):
    """Create new team"""
    db_team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db_session)
):
    """Get team by ID"""
    db_team = db.query(Team).filter(Team.TeamID == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team: TeamUpdate,
    db: Session = Depends(get_db_session)
):
    """Update team"""
    db_team = db.query(Team).filter(Team.TeamID == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    for field, value in team.model_dump(exclude_unset=True).items():
        setattr(db_team, field, value)
    
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/{team_id}", response_model=TeamResponse)
def delete_team(
    team_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete team"""
    db_team = db.query(Team).filter(Team.TeamID == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_team)
    db.commit()
    return db_team

# Team member management endpoints
@router.post("/{team_id}/members", response_model=TeamResponse)
def add_team_member(
    team_id: int,
    member: TeamMemberBase,
    db: Session = Depends(get_db_session)
):
    """Add member to team"""
    db_team = db.query(Team).filter(Team.TeamID == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_member = TeamMember(**member.model_dump(), TeamID=team_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/{team_id}/members/{employee_id}", response_model=TeamResponse)
def remove_team_member(
    team_id: int,
    employee_id: int,
    db: Session = Depends(get_db_session)
):
    """Remove member from team"""
    db_member = db.query(TeamMember).filter(
        TeamMember.TeamID == team_id,
        TeamMember.EmployeeID == employee_id
    ).first()
    
    if not db_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    db.delete(db_member)
    db.commit()
    
    return db.query(Team).filter(Team.TeamID == team_id).first() 