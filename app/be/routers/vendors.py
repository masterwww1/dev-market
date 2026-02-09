"""Vendor API for B2B marketplace."""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from be.database import get_db
from be.models.vendor import Vendor
from be.schemas.vendor import VendorCreate, VendorResponse

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("/", response_model=List[VendorResponse])
def list_vendors(db: Session = Depends(get_db)) -> List[Vendor]:
    """List all vendors."""
    return db.query(Vendor).order_by(Vendor.created_at.desc()).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VendorResponse)
def create_vendor(body: VendorCreate, db: Session = Depends(get_db)) -> Vendor:
    """Create a new vendor."""
    vendor = Vendor(name=body.name)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor
