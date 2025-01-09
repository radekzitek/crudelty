from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import TimestampMixin
from ..core.db import Base

class Organization(Base, TimestampMixin):
    __tablename__ = "Organization"

    OrganizationID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False, index=True)
    Address = Column(Text)
    Phone = Column(String(50))
    Email = Column(String(255))
    Website = Column(String(255))
    TopDepartmentID = Column(BigInteger, ForeignKey("Department.DepartmentID"))

    # Relationships
    departments = relationship("Department", back_populates="organization", foreign_keys="Department.OrganizationID")
    employees = relationship("Employee", back_populates="organization")
    teams = relationship("Team", back_populates="organization")
    top_department = relationship("Department", foreign_keys=[TopDepartmentID])

class Department(Base, TimestampMixin):
    __tablename__ = "Department"

    DepartmentID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False, index=True)
    Description = Column(Text)
    ParentDepartmentID = Column(BigInteger, ForeignKey("Department.DepartmentID"))
    HeadOfDepartmentID = Column(BigInteger, ForeignKey("Employee.EmployeeID"))
    OrganizationID = Column(BigInteger, ForeignKey("Organization.OrganizationID"), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="departments", foreign_keys=[OrganizationID])
    parent = relationship("Department", remote_side=[DepartmentID], backref="subdepartments")
    head = relationship("Employee", foreign_keys=[HeadOfDepartmentID])
    positions = relationship("PositionJob", back_populates="department")

class Employee(Base, TimestampMixin):
    __tablename__ = "Employee"

    EmployeeID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False, index=True)
    Email = Column(String(255), nullable=False, unique=True)
    Phone = Column(String(50))
    OrganizationID = Column(BigInteger, ForeignKey("Organization.OrganizationID"), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="employees")
    positions = relationship("PositionJob", secondary="EmployeePosition", back_populates="employees")
    teams = relationship("Team", secondary="TeamMember", back_populates="members")

class PositionJob(Base, TimestampMixin):
    __tablename__ = "PositionJob"

    PositionID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False, index=True)
    Description = Column(Text)
    DepartmentID = Column(BigInteger, ForeignKey("Department.DepartmentID"), nullable=False)

    # Relationships
    department = relationship("Department", back_populates="positions")
    employees = relationship("Employee", secondary="EmployeePosition", back_populates="positions")

class Team(Base, TimestampMixin):
    __tablename__ = "Team"

    TeamID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False, index=True)
    Description = Column(Text)
    TeamLeaderID = Column(BigInteger, ForeignKey("Employee.EmployeeID"))
    ParentTeamID = Column(BigInteger, ForeignKey("Team.TeamID"))
    OrganizationID = Column(BigInteger, ForeignKey("Organization.OrganizationID"), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="teams")
    leader = relationship("Employee", foreign_keys=[TeamLeaderID])
    parent = relationship("Team", remote_side=[TeamID], backref="subteams")
    members = relationship("Employee", secondary="TeamMember", back_populates="teams")

class EmployeePosition(Base, TimestampMixin):
    __tablename__ = "EmployeePosition"

    EmployeeID = Column(BigInteger, ForeignKey("Employee.EmployeeID"), primary_key=True)
    PositionID = Column(BigInteger, ForeignKey("PositionJob.PositionID"), primary_key=True)
    StartDate = Column(Date)
    EndDate = Column(Date)

class TeamMember(Base, TimestampMixin):
    __tablename__ = "TeamMember"

    TeamID = Column(BigInteger, ForeignKey("Team.TeamID"), primary_key=True)
    EmployeeID = Column(BigInteger, ForeignKey("Employee.EmployeeID"), primary_key=True)
    JoinDate = Column(Date) 