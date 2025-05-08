from fastapi_pagination import add_pagination
import uvicorn
from fastapi.staticfiles import StaticFiles
import uvicorn, os
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware  # required by google oauth

from api.utils.json_response import JsonResponseDict
from api.utils.logger import logger
from api.v1.routes import api_version_one
from api.utils.settings import settings

import subprocess
from alembic.config import Config
from alembic import command
from api.db.database import create_database

#views Dependencies
from fastapi.responses import HTMLResponse
from api.utils.config import templates_env

from api.db.database import get_db as db
from api.v1.services.user import user_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    #run_migrations()
    #create_database()
    yield


app = FastAPI(lifespan=lifespan)
add_pagination(app)


def run_migrations():
    # Load Alembic configuration from alembic.ini
    alembic_cfg = Config("alembic.ini")
    
    # Run migrations
    try:
        command.upgrade(alembic_cfg, "head")
        print("Alembic migration applied successfully.")
    except Exception as e:
        print(f"Error running Alembic migration: {e}")


'''@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs at startup
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Alembic migration applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error applying Alembic migration: {e}")

    yield  # Let the application run

app = FastAPI(lifespan=lifespan)'''

# Set up email templates and css static files
email_templates = Jinja2Templates(directory='api/core/dependencies/email/templates')

'''# MEDIA_DIR = os.path.expanduser('~/.media')
MEDIA_DIR = './media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Load up media static files
app.mount('/media', StaticFiles(directory=MEDIA_DIR), name='media')'''

# Define the temporary directory
MEDIA_DIR = '/tmp/media'

try:
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
except Exception as e:
    print(f"Error creating media directory: {e}")
    pass  # Ignore the error and continue

# Mount the media directory to serve static files
try:
    app.mount('/media', StaticFiles(directory=MEDIA_DIR), name='media')
except Exception as e:
    print(f"Error mounting media directory: {e}")
    pass  # Ignore the error and continue


origins = [
   "*"
]


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_version_one)

@app.get("/api", tags=["Api Home"])
async def get_root(request: Request) -> dict:
    return JsonResponseDict(
        message="Welcome to OptiCheck API", status_code=status.HTTP_200_OK, data={"URL": ""}
    )


@app.get("/probe", tags=["Home"])
async def probe():
    return {"message": "I am the Python FastAPI API responding"}


# REGISTER EXCEPTION HANDLERS
@app.exception_handler(HTTPException)
async def http_exception(request: Request, exc: HTTPException):
    """HTTP exception handler"""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception(request: Request, exc: RequestValidationError):
    """Validation exception handler"""

    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "status_code": 422,
            "message": "Invalid input",
            "errors": errors,
        },
    )


@app.exception_handler(IntegrityError)
async def exception(request: Request, exc: IntegrityError):
    """Integrity error exception handlers"""

    logger.exception(f"Exception occured; {exc}")

    return JSONResponse(
        status_code=400,
        content={
            "status": False,
            "status_code": 400,
            "message": f"An unexpected error occurred: {exc}",
        },
    )


@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    """Other exception handlers"""

    logger.exception(f"Exception occured; {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "status_code": 500,
            "message": f"An unexpected error occurred: {exc}",
        },
    )


STATIC_DIR = "static/profile_images"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")




STATIC_DIR = '/tmp/static'  # Ensure STATIC_DIR is also in a writable location
try:
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
except Exception as e:
    print(f"Error creating static directory: {e}")
    pass  # Ignore the error and continue

try:
    app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
except Exception as e:
    print(f"Error mounting directories: {e}")
    pass 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) 

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
    #uvicorn.run("main:app", host="0.0.0.0", port=7001, reload=True)
