from pydantic import BaseModel
from enums import ArticleTypes


class ArticlePayload(BaseModel):
    text: str
    article_type: ArticleTypes = ArticleTypes.RANDOM_FACT
