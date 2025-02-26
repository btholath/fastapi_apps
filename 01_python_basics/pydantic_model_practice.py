"""
Your goal is to create a social media post model using pydantic. The model should have:
An author, which is a string
An optional co-author, which is a string
A date, which is a string
A title, which is a string
The content, which is a string
An ID, which is an integer
Likes, which is a list of strings

The post should also have a field for comments, which is a list of comment models. The model should have:
An author, which is a string
The comment, which is a string
Likes, which is an integer

Practice creating a social media post with whatever data you like, so long as it compiles.
"""
from typing import Optional, List

from pydantic import BaseModel

class Comment(BaseModel):
    author: str
    comment: str
    likes: int

comments = [
    Comment(author="johnson", comment="Testing Pydantic!", likes=10)
]

class SocialMediaPostModel(BaseModel):
    author: str
    co_author: Optional[str]=None
    date: str
    title: str
    content: str
    id: int
    likes: List[str]
    comments: List[Comment]


post = SocialMediaPostModel(
    author="johnson",
    co_author="johnson",
    date="2021-01-10",
    title="Testing Pydantic!",
    content="Testing Pydantic!",
    id=1,
    likes=[],
    comments=comments
)

print(post)