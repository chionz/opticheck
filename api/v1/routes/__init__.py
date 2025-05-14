from fastapi import APIRouter
from api.v1.routes.auth import auth
from api.v1.routes.user import user_router
from api.v1.routes.eye_tests import eye_routes
from api.v1.routes.dashboard import dash_routes
from api.v1.routes.request_password import pwd_reset

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(auth)

api_version_one.include_router(pwd_reset)
api_version_one.include_router(user_router)
api_version_one.include_router(eye_routes)
api_version_one.include_router(dash_routes)