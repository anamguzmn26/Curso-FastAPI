from sqlalchemy import text
from .engine import engine

class DomainIndexes:
    @staticmethod
    def create_product_indexes():
        indexes = [
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_productos_nombre_disponible ON productos(nombre, descripcion, disponible);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_inventario_producto_stock ON inventario(producto_id, stock_actual, fecha_actualizacion DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transacciones_fecha_total ON transacciones(fecha_transaccion DESC, total);"
        ]
        with engine.connect() as connection:
            for sql in indexes:
                try:
                    connection.execute(text(sql))
                    print(f"Índice creado: {sql[:60]}...")
                except Exception as e:
                    print(f"Error creando índice: {e}")
