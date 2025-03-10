from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# URL de la base de datos
#DATABASE_URL = DATABASE_URL

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión
SessionLocal = sessionmaker(bind=engine)

# Base para modelos
Base = declarative_base()
