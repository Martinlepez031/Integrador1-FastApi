from fastapi import FastAPI

from app.core.database import Base, engine

from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.ventas.routers import router as ventas_router

# Importamos los modelos para que SQLAlchemy los registre
from app.modules.producto.models import Producto
from app.modules.categoria.models import Categoria
from app.modules.ventas.models import Venta


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integrador Lepez Martin - Unidad 2",
        description="Integración con base de datos PostgreSQL.",
        version="2.0.0"
    )

    @app.on_event("startup")
    def startup():
        Base.metadata.create_all(bind=engine)

    @app.get("/")
    def home():
        return {
            "message": "API Integrador funcionando correctamente con PostgreSQL",
            "docs": "/docs",
            "redoc": "/redoc"
        }

    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(ventas_router)

    return app


app = create_app()