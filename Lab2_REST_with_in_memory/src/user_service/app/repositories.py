from app.models import UserEntity
from app.database_memory import USER_LIST

class UserRepository:
    def create_user(self, user: UserEntity):
        USER_LIST.append(user)
        print(*USER_LIST)
        
    def get_all_users(self) -> list[UserEntity]:
        return USER_LIST