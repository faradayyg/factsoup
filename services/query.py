from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Article


def get_article_by_id(id: int, session: Session) -> Article:
    statement = select(Article).where(Article.id == id)
    result = session.execute(statement).fetchone()

    if not result:
        raise HTTPException(
            status_code=404, detail="The article you are looking for does not exist"
        )

    return result[0]
