"""Vendor API for B2B marketplace."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from be.database import get_db
from be.models.vendor import Vendor
from be.schemas.vendor import VendorCreate, VendorResponse, VendorUpdate

router = APIRouter(prefix="/vendors", tags=["Vendors"])


def _get_vendor_or_404(vendor_id: int, db: Session) -> Vendor:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    return vendor


@router.get("/", response_model=List[VendorResponse])
def list_vendors(db: Session = Depends(get_db)) -> List[Vendor]:
    """List all vendors."""
    return db.query(Vendor).order_by(Vendor.created_at.desc()).all()


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)) -> Vendor:
    """Get a vendor by id."""
    return _get_vendor_or_404(vendor_id, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VendorResponse)
def create_vendor(body: VendorCreate, db: Session = Depends(get_db)) -> Vendor:
    """Create a new vendor."""
    vendor = Vendor(name=body.name)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@router.patch("/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, body: VendorUpdate, db: Session = Depends(get_db)) -> Vendor:
    """Update a vendor (partial)."""
    vendor = _get_vendor_or_404(vendor_id, db)
    if body.name is not None:
        vendor.name = body.name
    db.commit()
    db.refresh(vendor)
    return vendor


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a vendor."""
    vendor = _get_vendor_or_404(vendor_id, db)
    db.delete(vendor)
    db.commit()
