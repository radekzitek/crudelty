from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .base import TimestampSchema

# Organization schemas
class OrganizationBase(BaseModel):
    Name: str
    Address: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[EmailStr] = None
    Website: Optional[str] = None
    TopDepartmentID: Optional[int] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    Name: Optional[str] = None

class OrganizationResponse(OrganizationBase, TimestampSchema):
    OrganizationID: int

# Department schemas
class DepartmentBase(BaseModel):
    Name: str
    Description: Optional[str] = None
    ParentDepartmentID: Optional[int] = None
    HeadOfDepartmentID: Optional[int] = None
    OrganizationID: int

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    Name: Optional[str] = None
    OrganizationID: Optional[int] = None

class DepartmentResponse(DepartmentBase, TimestampSchema):
    DepartmentID: int

# Employee schemas
class EmployeeBase(BaseModel):
    Name: str
    Email: EmailStr
    Phone: Optional[str] = None
    OrganizationID: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    Name: Optional[str] = None
    Email: Optional[EmailStr] = None
    OrganizationID: Optional[int] = None

class EmployeeResponse(EmployeeBase, TimestampSchema):
    EmployeeID: int

# Position schemas
class PositionBase(BaseModel):
    Name: str
    Description: Optional[str] = None
    DepartmentID: int

class PositionCreate(PositionBase):
    pass

class PositionUpdate(PositionBase):
    Name: Optional[str] = None
    DepartmentID: Optional[int] = None

class PositionResponse(PositionBase, TimestampSchema):
    PositionID: int

# Team schemas
class TeamBase(BaseModel):
    Name: str
    Description: Optional[str] = None
    TeamLeaderID: Optional[int] = None
    ParentTeamID: Optional[int] = None
    OrganizationID: int

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    Name: Optional[str] = None
    OrganizationID: Optional[int] = None

class TeamResponse(TeamBase, TimestampSchema):
    TeamID: int

# Junction table schemas
class EmployeePositionBase(BaseModel):
    EmployeeID: int
    PositionID: int
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None

class TeamMemberBase(BaseModel):
    TeamID: int
    EmployeeID: int
    JoinDate: Optional[date] = None 