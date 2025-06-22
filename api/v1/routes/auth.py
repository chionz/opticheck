from datetime import timedelta
from fastapi import (
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
    APIRouter,
    Response,
    Request,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import base58

from api.utils.success_response import success_response
from api.core.dependencies.email_sender import send_email
from api.utils.send_mail import send_magic_link
from api.v1.schemas.user import Token, LoginRequest, UserCreate, EmailRequest, WalletLoginPayload
from api.v1.schemas.token import TokenRequest, refreshToken
from api.v1.schemas.user import MagicLinkRequest
from api.db.database import get_db
from api.v1.models.user import User
from api.v1.services.user import user_service
from api.v1.services.auth import AuthService

auth = APIRouter(prefix="/auth", tags=["Authentication"])


@auth.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=success_response
)
def register(
    background_tasks: BackgroundTasks,
    response: Response,
    user_schema: UserCreate,
    db: Session = Depends(get_db),
):
    """Endpoint for a user to register their account"""

    # Create user account
    user = user_service.create(db=db, schema=user_schema)

    # Create access and refresh tokens
    access_token = user_service.create_access_token(user_id=user.id)
    refresh_token = user_service.create_refresh_token(user_id=user.id)

    
    response = success_response(
        status_code=201,
        message="User created successfully",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": jsonable_encoder(
                user,
                exclude=[
                    "password",
                    "is_super_admin",
                    "is_deleted",
                    "is_verified",
                    "updated_at",
                ],
            ),
        },
    )

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=60),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

@auth.post("/admin/login", status_code=status.HTTP_200_OK, response_model=success_response)
def adminlogin(
    background_tasks: BackgroundTasks,
    login_request: LoginRequest,
    db: Session = Depends(get_db),
):
    """Endpoint to log in a user"""

    # Authenticate the user
    user = user_service.authenticate_user(
        db=db, email=login_request.email, password=login_request.password
    )

    # Check if user is not an admin
    if not user.is_super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this route",
        )

    # Generate access and refresh tokens
    access_token = user_service.create_access_token(user_id=user.id)
    refresh_token = user_service.create_refresh_token(user_id=user.id)
    
    # Prepare the response data
    response = success_response(
        status_code=200,
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": jsonable_encoder(
                user,
                exclude=[
                    "password",
                    "is_super_admin",
                    "is_deleted",
                    "is_verified",
                    "updated_at",
                ],
            ),
        },
    )

     # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return response


@auth.post("/login", status_code=status.HTTP_200_OK, response_model=success_response)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db),
):
    """Endpoint to log in a user"""

    # Authenticate the user
    user = user_service.authenticate_user(
        db=db, email=login_request.email, password=login_request.password
    )

    # Generate access and refresh tokens
    access_token = user_service.create_access_token(user_id=user.id)
    refresh_token = user_service.create_refresh_token(user_id=user.id)
    response = success_response(
        status_code=200,
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": jsonable_encoder(
                user,
                exclude=[
                    "password",
                    "is_super_admin",
                    "is_deleted",
                    "is_verified",
                    "updated_at",
                ],
            ),
        },
    )

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response


@auth.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    response: Response, current_user: User = Depends(user_service.get_current_user)
):
    """Endpoint to log a user out of their account"""

    response = success_response(status_code=200, message="User logged out successfully")

    # Delete refresh token from cookies
    response.delete_cookie(key="refresh_token")

    return response


@auth.post("/refresh-access-token", status_code=status.HTTP_200_OK)
def refresh_access_token(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    """Endpoint to refresh access and refresh tokens"""

    # Get refresh token
    current_refresh_token = request.cookies.get("refresh_token")

    # Create new access and refresh tokens
    access_token, refresh_token = user_service.refresh_access_token(
        current_refresh_token=current_refresh_token
    )

    response = success_response(
        status_code=200,
        message="Tokens refreshed successfully",
        data={
            "access_token": access_token,
            "token_type": "bearer",
        },
    )

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response

@auth.post("/token")
def get_access_token(
    #request: Request, 
    # response: Response, 
    refresh_token: refreshToken):
    #current_refresh_token = request.cookies.get("refresh_token")
    new_access_token, new_refresh_token = user_service.refresh_access_token(
        current_refresh_token = refresh_token
    )
    #response.set_cookie(key="access_token", value=new_access_token, httponly=True)
    #response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"access_token": new_access_token, "refresh_token": new_refresh_token}

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


@auth.post("/wallet-login")
def wallet_login(payload: WalletLoginPayload, db: Session = Depends(get_db)):

    try:
        public_key_bytes = base58.b58decode(payload.public_key)
        signature_bytes = base58.b58decode(payload.signature)

        verify_key = VerifyKey(public_key_bytes)

        verify_key.verify(payload.message.encode(), signature_bytes)

    except (BadSignatureError, ValueError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature. Wallet verification failed.",
        )
    

    user = user_service.create_by_wallet(db=db, schema=payload)

    # Create access and refresh tokens
    access_token = user_service.create_access_token(user_id=user.id)
    refresh_token = user_service.create_refresh_token(user_id=user.id)

    response = success_response(
        status_code=201,
        message="User Authentication successfully",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": jsonable_encoder(
                user,
                exclude=[
                    "password",
                    "is_super_admin",
                    "is_deleted",
                    "is_verified",
                    "updated_at",
                ],
            ),
        },
    )

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=60),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response


@auth.get("/available-wallets")
def available_wallets():
    wallets = [
                {
                    "name": "Phantom",
                    "icon": "https://lcdevuaqwaynmlhtpmuo.supabase.co/storage/v1/object/public/walletimages//phantom.png",
                    "url": "https://phantom.app"
                },
                {
                    "name": "Solflare",
                    "icon": "https://lcdevuaqwaynmlhtpmuo.supabase.co/storage/v1/object/public/walletimages//solflare.webp",
                    "url": "https://solflare.com"
                },
                {
                    "name": "Slope",
                    "icon": "https://lcdevuaqwaynmlhtpmuo.supabase.co/storage/v1/object/public/walletimages//slope.png",
                    "url": "https://slope.finance"
                },
                {
                    "name": "Exodus",
                    "icon": "https://lcdevuaqwaynmlhtpmuo.supabase.co/storage/v1/object/public/walletimages//exodus.png",
                    "url": "https://www.exodus.com"
                },
                {
                    "name": "Ledger",
                    "icon": "https://lcdevuaqwaynmlhtpmuo.supabase.co/storage/v1/object/public/walletimages//ledger.svg",
                    "url": "https://www.ledger.com"
                }
    ]

    return {
        "wallets": wallets
            }