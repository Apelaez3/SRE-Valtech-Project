from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

from app.core.config import Config

# Crear engine (si usas SQLite, ese connect_args está bien)
engine = create_engine(Config().db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base declarativa como VARIABLE, NO como class
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
