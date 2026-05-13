from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambiá TU_PASSWORD por tu contraseña real de PostgreSQL
DATABASE_URL = "postgresql://postgres:admin22@localhost:5432/integrador2_db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()