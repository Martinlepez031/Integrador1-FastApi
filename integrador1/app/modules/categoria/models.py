from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(6), unique=True, index=True, nullable=False)
    descripcion = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)