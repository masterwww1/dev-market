"""Product API for B2B marketplace."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from be.database import get_db
from be.dependencies import CurrentUser, get_current_user
from be.models.product import Product
from be.models.vendor import Vendor
from be.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])
log = logging.getLogger(__name__)


def _get_product_or_404(product_id: int, db: Session) -> Product:
    """Get product by ID or raise 404."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        log.warning(f"⚠️ Product not found: product_id={product_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def _product_to_response(product: Product) -> ProductResponse:
    """Build ProductResponse from Product model (with joined vendor)."""
    return ProductResponse(
        id=product.id,
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price,
        vendor_id=product.vendor_id,
        vendor_name=product.vendor.name if product.vendor else None,
        created_at=product.created_at,
    )


@router.get("/", response_model=List[ProductResponse])
def list_products(
    vendor_id: Optional[int] = Query(None, gt=0, description="Filter by vendor ID"),
    db: Session = Depends(get_db),
) -> List[ProductResponse]:
    """List all products, optionally filtered by vendor."""
    try:
        log.info("📋 Listing products" + (f" (vendor_id={vendor_id})" if vendor_id else ""))
        q = db.query(Product).order_by(Product.created_at.desc())
        if vendor_id is not None:
            q = q.filter(Product.vendor_id == vendor_id)
        products = q.all()
        log.info(f"✅ Found {len(products)} product(s)")
        return [_product_to_response(p) for p in products]
    except Exception as e:
        log.error(f"❌ Error listing products: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products",
        )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponse:
    """Get a product by id."""
    try:
        log.info(f"🔍 Getting product: product_id={product_id}")
        product = _get_product_or_404(product_id, db)
        log.info(f"✅ Found product: product_id={product_id}, name={product.name}")
        return _product_to_response(product)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error getting product {product_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve product",
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(
    body: ProductCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ProductResponse:
    """Create a new product. Vendor is matched by user email == vendor email."""
    vendor = (
        db.query(Vendor)
        .filter(func.lower(Vendor.email) == current_user.email.lower())
        .first()
    )
    if not vendor:
        log.warning(f"⚠️ No vendor with matching email: user_id={current_user.id}, email={current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendor accounts can add products. No vendor found with your email.",
        )
    try:
        log.info(f"➕ Creating product: name={body.name}, vendor_id={vendor.id}")
        product = Product(
            name=body.name,
            sku=body.sku,
            description=body.description,
            price=body.price,
            vendor_id=vendor.id,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        log.info(f"✅ Product created: product_id={product.id}, name={product.name}")
        return _product_to_response(product)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error creating product: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        )


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, body: ProductUpdate, db: Session = Depends(get_db)
) -> ProductResponse:
    """Update a product (partial)."""
    try:
        log.info(f"✏️ Updating product: product_id={product_id}")
        product = _get_product_or_404(product_id, db)
        updates = body.model_dump(exclude_unset=True)
        if "vendor_id" in updates:
            vendor = db.query(Vendor).filter(Vendor.id == updates["vendor_id"]).first()
            if not vendor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
        for key, value in updates.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        log.info(f"✅ Product updated: product_id={product_id}")
        return _product_to_response(product)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error updating product {product_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product",
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a product."""
    try:
        log.info(f"🗑️ Deleting product: product_id={product_id}")
        product = _get_product_or_404(product_id, db)
        product_name = product.name
        db.delete(product)
        db.commit()
        log.info(f"✅ Product deleted: product_id={product_id}, name={product_name}")
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"❌ Error deleting product {product_id}: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product",
        )
