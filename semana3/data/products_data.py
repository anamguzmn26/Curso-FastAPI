from datetime import datetime
from typing import Dict, List, Optional
from models.product_models import CategoryEnum


# Simulación de una base de datos en memoria
products_db: Dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Laptop Gaming",
        "price": 1299.99,
        "description": "Laptop para gaming de alta performance",
        "category": CategoryEnum.electronics,
        "in_stock": True,
        "stock_quantity": 15,
        "created_at": datetime(2025, 7, 20, 10, 0, 0),
        "updated_at": None
    },
    2: {
        "id": 2,
        "name": "Camiseta Algodón",
        "price": 29.99,
        "description": "Camiseta 100% algodón, muy cómoda",
        "category": CategoryEnum.clothing,
        "in_stock": True,
        "stock_quantity": 50,
        "created_at": datetime(2025, 7, 21, 14, 30, 0),
        "updated_at": None
    }
}

# Contador para IDs autoincrementales
next_id = 3

def get_next_id() -> int:
    """Genera un ID autoincremental"""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

def get_all_products() -> List[dict]:
    """Devuelve todos los productos"""
    return list(products_db.values())

def get_product_by_id(product_id: int) -> Optional[dict]:
    """Busca un producto por su ID"""
    return products_db.get(product_id)

def create_product(product_data: dict) -> dict:
    """Crea un producto nuevo"""
    product_id = get_next_id()
    new_product = {
        "id": product_id,
        **product_data,
        "created_at": datetime.now(),
        "updated_at": None
    }
    products_db[product_id] = new_product
    return new_product

def update_product(product_id: int, product_data: dict) -> Optional[dict]:
    """Actualiza un producto existente"""
    if product_id in products_db:
        updated_product = {
            **products_db[product_id],
            **product_data,
            "updated_at": datetime.now()
        }
        products_db[product_id] = updated_product
        return updated_product
    return None

def delete_product(product_id: int) -> bool:
    """Elimina un producto"""
    if product_id in products_db:
        del products_db[product_id]
        return True
    return False
