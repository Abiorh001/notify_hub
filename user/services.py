from .schema import User, UserResponse
from fastapi import HTTPException, status, APIRouter


@dataclass
class UserService:
    def create_user(self, user: User) -> UserResponse:
        return UserResponse(username=user.username, email=user.email, is_active=user.is_active)