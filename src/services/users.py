
from db.database import db
from db.repositories.users import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None
    
    def register_user(self, username: str, email: str, password: str):
        if self.user_repo.exists_by_email(email):
            return None, "Пользователь с таким email уже существует"
        
        if self.user_repository.exists_by_username(username):
            return None, "Пользователь с таким именем уже существует"

        user = User(username=username, email=email)
        user.set_password(password)

        created_user = self.user_repository.create_user(
            username=username,
            email=email,
            password_hash=user.password_hash
        )
        
        return created_user, "Регистрация прошла успешно"

    def get_user_by_id(self, user_id: int):
        return self.user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self.user_repository.get_by_email(email)
