from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Settings

settings = Settings()

# Crear el motor de base de datos
engine = create_engine(
    settings.DATABASE_URL
)

# Crear una clase de sesión local
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para las clases de modelos
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
