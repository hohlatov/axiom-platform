from fastapi import APIRouter, Depends
from app.models.user import User
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active
    }