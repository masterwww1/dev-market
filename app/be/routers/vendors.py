"""Vendor API for B2B marketplace."""
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from be.database import get_db
from be.models.vendor import Vendor
from be.schemas.vendor import VendorCreate, VendorResponse, VendorUpdate

router = APIRouter(prefix="/vendors", tags=["Vendors"])
log = logging.getLogger(__name__)


def _get_vendor_or_404(vendor_id: int, db: Session) -> Vendor:
    """Get vendor by ID or raise 404."""
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        log.warning(f"⚠️ Vendor not found: vendor_id={vendor_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    return vendor


@router.get("/", response_model=List[VendorResponse])
def list_vendors(db: Session = Depends(get_db)) -> List[Vendor]:
    """List all vendors."""
    try:
        log.info("📋 Listing all vendors")
        vendors = db.query(Vendor).order_by(Vendor.created_at.desc()).all()
        log.info(f"✅ Found {len(vendors)} vendor(s)")
        return vendors
    except Exception as e:
        log.error(f"❌ Error listing vendors: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vendors",
        )


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)) -> Vendor:
    """Get a vendor by id."""
    try:
        log.info(f"🔍 Getting vendor: vendor_id={vendor_id}")
        vendor = _get_vendor_or_404(vendor_id, db)
        log.info(f"✅ Found vendor: vendor_id={vendor_id}, name={vendor.name}")
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error getting vendor {vendor_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vendor",
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VendorResponse)
def create_vendor(body: VendorCreate, db: Session = Depends(get_db)) -> Vendor:
    """Create a new vendor."""
    try:
        log.info(f"➕ Creating vendor: name={body.name}")
        vendor = Vendor(
            name=body.name,
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            phone_number=body.phone_number,
        )
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
        log.info(f"✅ Vendor created successfully: vendor_id={vendor.id}, name={vendor.name}")
        return vendor
    except Exception as e:
        log.error(f"❌ Error creating vendor: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create vendor",
        )


@router.patch("/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, body: VendorUpdate, db: Session = Depends(get_db)) -> Vendor:
    """Update a vendor (partial)."""
    try:
        log.info(f"✏️ Updating vendor: vendor_id={vendor_id}, updates={body.model_dump(exclude_unset=True)}")
        vendor = _get_vendor_or_404(vendor_id, db)
        old_name = vendor.name
        
        if body.name is not None:
            vendor.name = body.name
        if body.first_name is not None:
            vendor.first_name = body.first_name
        if body.last_name is not None:
            vendor.last_name = body.last_name
        if body.email is not None:
            vendor.email = body.email
        if body.phone_number is not None:
            vendor.phone_number = body.phone_number
        
        db.commit()
        db.refresh(vendor)
        log.info(f"✅ Vendor updated: vendor_id={vendor_id}, old_name={old_name}, new_name={vendor.name}")
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error updating vendor {vendor_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update vendor",
        )


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a vendor."""
    try:
        log.info(f"🗑️ Deleting vendor: vendor_id={vendor_id}")
        vendor = _get_vendor_or_404(vendor_id, db)
        vendor_name = vendor.name
        db.delete(vendor)
        db.commit()
        log.info(f"✅ Vendor deleted: vendor_id={vendor_id}, name={vendor_name}")
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error deleting vendor {vendor_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete vendor",
        )
