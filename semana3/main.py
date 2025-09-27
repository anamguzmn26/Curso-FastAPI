from fastapi import FastAPI, HTTPException, Query, Path, status
from typing import Optional
from models.product_models import (
    ProductResponse, ProductCreate, ProductUpdate, CategoryEnum
)
from data.products_data import (
    get_all_products, get_product_by_id
)
# semana3/main.py

app = FastAPI(
    title="API de Inventario - Semana 3",
    description="API REST completa para manejo de productos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 🚀 Endpoint raíz
@app.get("/", summary="Endpoint de bienvenida")
async def root():
    return {
        "message": "API de Inventario - Semana 3",
        "version": "1.0.0",
        "docs": "/docs"
    }

# 🚀 GET: Listar todos los productos
@app.get(
    "/products",
    summary="Obtener lista de productos",
    description="Obtiene una lista de todos los productos"
)
async def get_products():
    products = get_all_products()
    return {"total": len(products), "products": products}

# 🚀 GET: Obtener un producto por ID
@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto por ID",
    description="Devuelve la información de un producto según su ID"
)
async def get_product(product_id: int = Path(..., gt=0, description="ID del producto")):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    return ProductResponse(**product)
