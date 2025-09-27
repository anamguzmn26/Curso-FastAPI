from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.engine import get_db
from ..services.optimized_domain_service import OptimizedDomainService
from ..cache.cache_decorators import cache_result
from ..cache.invalidation import DomainCacheInvalidation
from sqlalchemy import text

router = APIRouter(prefix="/bakery_product", tags=["Productos"])

@router.get("/available")
@cache_result(ttl_type='frequent_data', key_prefix='bakery_stock')
def get_available_products(buscar: str = None, stock_min: int = 1, db: Session = Depends(get_db)):
    service = OptimizedDomainService(db, 'bakery_')
    return service.get_products_available(buscar=buscar, stock_min=stock_min)

@router.get("/stock-alerts")
def stock_alerts(db: Session = Depends(get_db)):
    service = OptimizedDomainService(db, 'bakery_')
    return service.get_stock_alerts()

@router.put("/update-stock/{product_id}")
def update_stock(product_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        new_stock = int(payload.get('stock_actual'))
    except Exception:
        raise HTTPException(status_code=400, detail="Payload debe incluir stock_actual (int)")
    db.execute(text("UPDATE inventario SET stock_actual = :new_stock WHERE producto_id = :product_id"),
               {'new_stock': new_stock, 'product_id': product_id})
    db.commit()
    DomainCacheInvalidation.on_entity_update(str(product_id), 'producto')
    return {"message": "Stock actualizado"}
