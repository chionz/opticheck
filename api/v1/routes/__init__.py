from fastapi import APIRouter
from api.v1.routes.auth import auth
from api.v1.routes.user import user_router
from api.v1.routes.facebook_login import fb_auth
from api.v1.routes.waitlist import waitlist as waitlist_router
from api.v1.routes.request_password import pwd_reset
from api.v1.routes.activity_logs import activity_logs
from api.v1.routes.advertisements import advert

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(auth)

api_version_one.include_router(fb_auth)
api_version_one.include_router(pwd_reset)
api_version_one.include_router(user_router)
api_version_one.include_router(activity_logs)
api_version_one.include_router(waitlist_router)
api_version_one.include_router(advert)