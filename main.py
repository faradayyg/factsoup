from fastapi import FastAPI
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from dtos import ArticlePayload
from models import Article
from dotenv import load_dotenv
from chat_gpt import generate_article as chat_gpt_generate_article

load_dotenv()

app = FastAPI()


def _generate_and_save_article(payload: ArticlePayload, session: Session) -> Article:
    chat_gpt_response = chat_gpt_generate_article(payload=payload)
    new_article_obj = Article(
        token_hash=hash(payload.text),
        token=payload.text,
        generated_article=chat_gpt_response,
    )
    session.add(new_article_obj)
    session.commit()
    return new_article_obj


def _get_or_create_article(payload: ArticlePayload, session: Session) -> str:
    # Create a hash from the token
    token_hash = hash(payload.text)
    print(token_hash)
    # Check if it exists
    statement = select(Article).where(
        or_(Article.token_hash == token_hash, Article.token == payload.text)
    )
    inter = session.execute(statement)
    article = inter.fetchone()
    if article is not None:
        return article[0].generated_article

    article = _generate_and_save_article(payload, session)
    return article.generated_article


@app.get("/")
def home():
    return {"msg": "hello"}


@app.post("/generate-article")
def generate_article(payload: ArticlePayload) -> dict[str, str]:
    from models import engine

    # Get article from cache or create
    session = Session(engine)
    print("Is something up?? \n" * 3)
    with session:
        article = _get_or_create_article(payload, session)
    return {"article": article}
