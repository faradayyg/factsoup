from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Integer, func, JSON
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[int] = mapped_column(Integer)
    token: Mapped[str] = mapped_column(String(250))
    generated_article: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    other_details: Mapped[str | None] = mapped_column(JSON)


engine = create_engine(os.getenv("DB_URL", "sqlite:///storage.db"), echo=True)
Base.metadata.create_all(engine)
