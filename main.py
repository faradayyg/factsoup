from fastapi import Depends, FastAPI
from sqlalchemy import engine, or_, select
from sqlalchemy.orm import Session
from dtos import ArticlePayload, ArticleResponseDTO
from models import Article
from dotenv import load_dotenv
from models import engine
from services.query import get_article_by_id
from fastapi.middleware.cors import CORSMiddleware
from services.chat_gpt import generate_article as chat_gpt_generate_article

load_dotenv()

app = FastAPI()


allowed_origins = ["*"] # TODO: get this from env os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()


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


def _get_or_create_article(payload: ArticlePayload, session: Session) -> Article:
    # Create a hash from the token
    token_hash = hash(payload.text)
    # Check if it exists
    statement = select(Article).where(
        or_(Article.token_hash == token_hash, Article.token == payload.text)
    )
    inter = session.execute(statement)
    article = inter.fetchone()
    if article is not None:
        return article[0]

    article = _generate_and_save_article(payload, session)
    return article


@app.get("/")
def home():
    return {"msg": "hello"}


@app.post("/generate-article/", response_model=ArticleResponseDTO)
def generate_article(
    payload: ArticlePayload, session: Session = Depends(get_session)
) -> ArticleResponseDTO:
    # Get article from cache or create
    article = _get_or_create_article(payload, session)

    return ArticleResponseDTO.model_validate(article)


@app.get("/article/{id}/", response_model=ArticleResponseDTO)
def get_article(id: int, session: Session = Depends(get_session)) -> ArticleResponseDTO:
    article = get_article_by_id(id, session)

    return ArticleResponseDTO.model_validate(article)
