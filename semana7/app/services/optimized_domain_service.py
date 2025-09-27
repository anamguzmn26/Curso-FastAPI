from sqlalchemy import text
from typing import List, Dict, Any

class OptimizedDomainService:
    def __init__(self, db, domain_prefix: str = 'bakery_'):
        self.db = db
        self.domain_prefix = domain_prefix

    def get_products_available(self, buscar: str = None, stock_min: int = 1) -> List[Dict]:
        query = """
            SELECT p.id, p.nombre, p.descripcion, p.precio, i.stock_actual
            FROM productos p
            JOIN inventario i ON p.id = i.producto_id
            WHERE i.stock_actual > :stock_min
            AND p.disponible = true
        """
        params = {"stock_min": stock_min}
        if buscar:
            query += " AND (p.nombre ILIKE '%' || :buscar || '%' OR p.descripcion ILIKE '%' || :buscar || '%')"
            params['buscar'] = buscar

        query += " ORDER BY p.nombre"

        result = self.db.execute(text(query), params)
        return [dict(r) for r in result]

    def get_stock_alerts(self, threshold_ratio: float = 1.2) -> List[Dict]:
        query = """
            SELECT p.id, p.nombre, i.stock_actual, i.stock_minimo,
                   (i.stock_actual::float / NULLIF(i.stock_minimo,0)) as ratio_stock
            FROM productos p
            JOIN inventario i ON p.id = i.producto_id
            WHERE i.stock_actual <= i.stock_minimo * :threshold_ratio
            AND p.disponible = true
            ORDER BY ratio_stock ASC
        """
        result = self.db.execute(text(query), {"threshold_ratio": threshold_ratio})
        return [dict(r) for r in result]
