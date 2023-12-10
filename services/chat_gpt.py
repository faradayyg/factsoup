from openai import OpenAI
import os
from dtos import ArticlePayload
import dataclasses


@dataclasses.dataclass
class PromptData:
    system_prompt: str
    user_prompt: str


def _generate_prompt(payload: ArticlePayload) -> PromptData:
    return PromptData(
        system_prompt="You are a helpful assistant for writing blog posts",
        user_prompt=f"Generate a 300 word article in markdown on the topic: '{payload.text}' in the category {payload.article_type}",
    )


def generate_article(payload: ArticlePayload) -> str | None:
    print("Beginning generation...")
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
    prompt = _generate_prompt(payload)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": prompt.system_prompt},
            {
                "role": "user",
                "content": prompt.user_prompt,
            },
        ],
    )
    print(response)
    return response.choices[0].message.content
