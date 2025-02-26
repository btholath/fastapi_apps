"""
imports your Pydantic models and then creates multiple test cases. The script demonstrates valid instantiations as well as several invalid scenarios that trigger validation errors. You can run this script to see how your models behave with different inputs.
"""

# !/usr/bin/env python3
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional


# Your Pydantic models
class Comment(BaseModel):
    author: str


class User(BaseModel):
    username: str
    password: Optional[str] = None
    likes: Dict[str, int]
    comments: List[Comment]


class AdminUser(User):
    admin_password: str


def main():
    print("---- Testing Comment ----")
    # Valid Comment instance
    try:
        comment = Comment(author="Alice")
        print("Valid Comment:", comment)
    except ValidationError as e:
        print("Validation Error in Comment:", e)

    # Invalid Comment: missing required 'author'
    try:
        comment_invalid = Comment()
        print("Invalid Comment created:", comment_invalid)
    except ValidationError as e:
        print("Expected Error for Comment (missing author):", e)

    print("\n---- Testing User ----")
    # Valid User instance (all required fields provided)
    try:
        user = User(
            username="bob",
            password="bobpass",
            likes={"Python": 10, "Pydantic": 5},
            comments=[Comment(author="Alice"), Comment(author="Bob")]
        )
        print("Valid User:", user)
    except ValidationError as e:
        print("Validation Error in User:", e)

    # Valid User with missing optional password (should default to None)
    try:
        user_no_password = User(
            username="charlie",
            likes={"Testing": 3},
            comments=[Comment(author="Eve")]
        )
        print("User with missing password (password defaults to None):", user_no_password)
    except ValidationError as e:
        print("Validation Error in User with missing password:", e)

    # Invalid User: 'likes' dict has a non-integer value
    try:
        user_invalid_likes = User(
            username="david",
            likes={"Python": "ten"},  # invalid: value should be an int
            comments=[Comment(author="Alice")]
        )
        print("User with invalid likes:", user_invalid_likes)
    except ValidationError as e:
        print("Expected Error for User (invalid likes):", e)

    # Invalid User: 'comments' is not a list of Comment instances
    try:
        user_invalid_comments = User(
            username="eve",
            likes={"Python": 5},
            comments="This is not a list"  # invalid: should be a list of Comment objects
        )
        print("User with invalid comments:", user_invalid_comments)
    except ValidationError as e:
        print("Expected Error for User (invalid comments):", e)

    print("\n---- Testing AdminUser ----")
    # Valid AdminUser instance
    try:
        admin = AdminUser(
            username="admin1",
            password="adminpass",
            likes={"Management": 100},
            comments=[Comment(author="CEO")],
            admin_password="supersecret"
        )
        print("Valid AdminUser:", admin)
    except ValidationError as e:
        print("Validation Error in AdminUser:", e)

    # Invalid AdminUser: missing required 'admin_password'
    try:
        admin_missing = AdminUser(
            username="admin2",
            password="pass",
            likes={"Management": 50},
            comments=[Comment(author="CTO")]
            # admin_password is missing
        )
        print("AdminUser with missing admin_password:", admin_missing)
    except ValidationError as e:
        print("Expected Error for AdminUser (missing admin_password):", e)

    # Testing extra fields (by default extra fields are ignored)
    try:
        user_extra = User(
            username="extra",
            likes={"Extra": 1},
            comments=[Comment(author="Someone")],
            extra_field="this field is not defined"  # extra field
        )
        print("User with extra field (extra_field is ignored):", user_extra)
    except ValidationError as e:
        print("Validation Error with extra field:", e)


if __name__ == '__main__':
    main()
