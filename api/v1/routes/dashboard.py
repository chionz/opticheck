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

""" @auth.get("/refresh-token")
def get_refresh_token(request: Request, response: Response):
    current_refresh_token = request.cookies.get("refresh_token")
    new_access_token, new_refresh_token = user_service.refresh_access_token(
        current_refresh_token
    )
    refresh_token = user_service.create_refresh_token(user_id)
    response.set_cookie(key="access_token", value=new_access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"access_token": new_access_token} """

# User Dashboard View
@dash_routes.post("/me")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = user_service.fetch_user_refresh_token(request, db=db)
    print("User_id:", user_id)
    if user_id == None:
        raise HTTPException(status_code=401, detail="no refresh token provided")
    user = user_service.get_user_by_id(db=db, id=user_id)


    """ current_refresh_token = request.cookies.get("refresh_token")
    if current_refresh_token == None:
        raise HTTPException(status_code=401, detail="no refresh token provided")
    
    token_data = user_service.verify_refresh_token(refresh_token=current_refresh_token)
    user_id =token_data.id
    user = user_service.get_user_by_id(db=db, id=user_id) """
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




# User Dashboard View
@dash_routes.post("/me1")
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
