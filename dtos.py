from pydantic import BaseModel, ConfigDict
from enums import ArticleTypes


class ArticlePayload(BaseModel):
    text: str
    article_type: ArticleTypes = ArticleTypes.RANDOM_FACT


class ArticleResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    token_hash: int
    generated_article: str
    token: str

