from typing import List
from app.schemas.user_schema import UserSchema

from faker import Faker

class UserController:

    def __init__(self):
        self.fake = Faker()

    def get_user(self, user_id: int) -> UserSchema:
        pass

    def create_user(self, user: UserSchema) -> UserSchema:
        return user

    def get_all_users(self) -> List[UserSchema]:
        
        response = []

        for i in range(5):
            response.append(UserSchema(
                id=i,
                name=self.fake.name(),
                email=self.fake.email()
            ))

        return response

