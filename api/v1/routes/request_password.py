from fastapi import APIRouter, Depends, HTTPException, Request, Query, BackgroundTasks, status
from sqlalchemy.orm import Session
from api.v1.models.user import User
from api.v1.schemas.request_password_reset import RequestEmail, ResetPassword, ChangePassword
from api.v1.schemas.user import ChangePasswordSchema
from api.db.database import get_db as get_session
from api.v1.services.request_pwd import reset_service, get_password_hash
from api.v1.services.user import user_service
from api.utils.success_response import success_response
from sqlalchemy.exc import SQLAlchemyError
import logging

pwd_reset = APIRouter(prefix="/auth", tags=["Password Authentication"])


# generate password reset link
@pwd_reset.post("/request-password-reset")
async def request_reset_link(
    reset_schema: RequestEmail,
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    return await reset_service.create(reset_schema, request, session, background_tasks)


# process password link
@pwd_reset.get("/reset-password")
async def process_reset_link(
    token: str = Query(...), session: Session = Depends(get_session)
):
    return reset_service.process_reset_link(token, session)



# change the password
@pwd_reset.post("/reset-password")
async def reset_password(
    data: ResetPassword,
    token: str = Query(...),
    session: Session = Depends(get_session),
):
    return reset_service.reset_password(data, token, session)


@pwd_reset.post("/change-password")
async def changepassword(
    data: ChangePassword,
    request: Request, db: Session = Depends(get_session),
):
    try:
        user_id = user_service.fetch_user_refresh_token(request, db=db)
        if user_id == None:
            return HTTPException(status_code=400, detail="Invalid or expired token")
        user = user_service.get_user_by_id(db=db, id=user_id)
        
        password = user_service.verify_password(data.old_password, user.password)
        if not password:
            return HTTPException(status_code=400, detail= "Current Password is incorrect" )
        if data.new_password != data.confirm_new_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        user = user_service.updatepassword(db=db, schema={"password":data.new_password}, id=user_id, current_user=user)
       
        return success_response(
            message="Password has been reset successfully",
            status_code=status.HTTP_200_OK,
        )

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session in case of an error
        print(f"Database error: {e}")  # Log the error for debugging purposes
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request.",
        )

