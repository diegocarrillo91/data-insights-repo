from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.schemas.user_schema import UserSchema, CreateUserSchema
from app.controllers.user_controller import UserController

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

user_controller = UserController()

@router.get("/", response_model=List[UserSchema])
async def read_users():
    return user_controller.get_all_users()

@router.post("/", response_model=UserSchema)
async def create_user(user: CreateUserSchema):

    user_schema = UserSchema(
        id=0,
        name=user.name,
        email=user.email
    )

    return user_controller.create_user(user_schema)