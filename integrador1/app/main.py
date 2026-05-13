from fastapi import FastAPI
from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.ventas.routers import router as ventas_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integrador Lepez Martin - Unidad 1",
        description="Conceptos: Path, Query, Body, Pydantic, Errores.",
        version="1.0.0"
    )

    @app.get("/")
    def home():
        return {
            "message": "API Integrador funcionando correctamente",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(ventas_router)
    
    return app

app = create_app()