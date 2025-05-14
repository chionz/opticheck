from fastapi import Depends, APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.utils.success_response import success_response
from api.v1.models.user import User

from api.db.database import get_db
from api.v1.services.user import user_service
from api.v1.services.eye_tests import eyetest_service


def dashboard_items(request: Request, db: Session = Depends(get_db)):
    user_id = user_service.fetch_user_refresh_token(request, db=db)

    if user_id == None:
        return None
    user = user_service.get_user_by_id(db=db, id=user_id)
    return {"user": user, "user_id": user_id}


dash_routes = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# User Dashboard View
@dash_routes.post("/me")
async def dashboard(refresh_token:str, request: Request, db: Session = Depends(get_db)):
    if refresh_token == None:
        raise HTTPException(status_code=401, detail="no refresh token provided")
    
    token_data = user_service.verify_refresh_token(refresh_token=refresh_token)
    user_id =token_data.id
    user = user_service.get_user_by_id(db=db, id=user_id)
    no_test_done = eyetest_service.all_test_count(db, user_id=user_id)
    vision = eyetest_service.dashboard_vision_test(db, user_id=user_id)
    # print(wallet, user)

    user = jsonable_encoder(
            user,
            exclude=[
                "password",
                "is_super_admin",
                "is_deleted",
                "is_verified",
                "updated_at",
            ],
    )
    return success_response(
        status_code=200,
        message="User details retrieved successfully",
        data= {
            "user": user,
            "test_taken": no_test_done,
            "eye_test_data": vision
        }
    )
