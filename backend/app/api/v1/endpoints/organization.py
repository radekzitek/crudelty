from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.db import get_db_session
from ....models.tables import Organization
from ....schemas.schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    responses={
        404: {"description": "Organization not found"},
        400: {"description": "Bad request"},
    }
)

@router.get(
    "/",
    response_model=List[OrganizationResponse],
    summary="List Organizations",
    description="""
    Retrieve a list of all organizations.
    
    - Supports pagination through skip/limit parameters
    - Returns a list of organizations with their basic information
    """,
    response_description="List of organizations"
)
def list_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
):
    """
    List all organizations with pagination support.
    
    Parameters:
    - skip: Number of records to skip (offset)
    - limit: Maximum number of records to return
    
    Returns:
    - List of organizations with their details
    """
    return db.query(Organization).offset(skip).limit(limit).all()

@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=201,
    summary="Create Organization",
    description="""
    Create a new organization with the provided details.
    
    Required fields:
    - Name: Organization name
    
    Optional fields:
    - Address: Physical address
    - Phone: Contact phone number
    - Email: Contact email address
    - Website: Organization website
    - TopDepartmentID: ID of the main department
    """,
    response_description="Created organization details"
)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db_session)
):
    """
    Create new organization
    
    Example request body:
    ```json
    {
        "Name": "Acme Corporation",
        "Address": "123 Business St, City, Country",
        "Phone": "+1234567890",
        "Email": "contact@acme.com",
        "Website": "https://acme.com"
    }
    ```
    """
    db_org = Organization(**organization.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@router.get(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Get Organization",
    description="""
    Retrieve detailed information about a specific organization by its ID.
    
    Includes:
    - Basic organization details
    - Contact information
    - Top department reference
    """,
    responses={
        404: {
            "description": "Organization not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Organization not found"}
                }
            }
        }
    }
)
def get_organization(
    org_id: int,
    db: Session = Depends(get_db_session)
):
    """
    Get organization by ID
    
    Parameters:
    - org_id: Organization ID (integer)
    
    Returns:
    - Organization details if found
    - 404 error if not found
    """
    db_org = db.query(Organization).filter(Organization.OrganizationID == org_id).first()
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org

@router.put(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Update Organization",
    description="""
    Update an existing organization's information.
    
    All fields are optional in the update request.
    Only provided fields will be updated.
    """,
    responses={
        404: {"description": "Organization not found"},
        400: {"description": "Invalid update data"}
    }
)
def update_organization(
    org_id: int,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db_session)
):
    """
    Update organization
    
    Example request body:
    ```json
    {
        "Name": "Acme Corp Updated",
        "Website": "https://acme-updated.com"
    }
    ```
    """
    db_org = db.query(Organization).filter(Organization.OrganizationID == org_id).first()
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    for field, value in organization.model_dump(exclude_unset=True).items():
        setattr(db_org, field, value)
    
    db.commit()
    db.refresh(db_org)
    return db_org

@router.delete(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Delete Organization",
    description="""
    Delete an organization and all related data.
    
    Warning: This operation will also delete:
    - All departments in the organization
    - All positions in those departments
    - All team memberships
    - All employee associations
    """,
    responses={
        404: {"description": "Organization not found"},
        409: {"description": "Cannot delete organization with active dependencies"}
    }
)
def delete_organization(
    org_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete organization"""
    db_org = db.query(Organization).filter(Organization.OrganizationID == org_id).first()
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    db.delete(db_org)
    db.commit()
    return db_org 