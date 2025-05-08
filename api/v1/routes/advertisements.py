from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params, add_pagination, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as pagination
from sqlalchemy.orm import Session
from api.utils.success_response import success_response
from api.v1 import schemas
from api.v1.models.advertisement import Advert
from api.v1.schemas.adverisements import AdvertCreate, AdvertResponse, AdvertUpdate
from api.db.database import get_db
from api.v1.services.user import user_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.v1.models.user import User
from api.v1.services.advertisements import Advert_service
from sqlalchemy.orm import joinedload

from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()
advert = APIRouter(prefix="/adverts", tags=["Adverts"])

# adds pagination to data output for adverts
add_pagination(advert)

#Helper Function to serialize data
def to_dict(obj):
    return{column.name: getattr(obj, column.name) for column in obj.__table__.columns}


# This Endpoint Creates adverts(Admins/Clients)
@advert.post("/create")
async def create_advert(
    schema: AdvertCreate,
    db: Session = Depends(get_db),
    current_user: User = Security(user_service.get_current_super_admin),
):
    # This creates the advert using advert service function
    create = Advert_service.create_advert(db, schema)

    return create


# This Serialize advert details
def serialize_advert(advert):
    return {
        "id": advert.id,
        "title": advert.title,
        "description": advert.description,
        "status": advert.status,
        "created_at": advert.created_at.isoformat(),
        "due_date": advert.due_date.isoformat() if advert.due_date else None,
        "priority":advert.priority,
    }


# This Endpoint Gets all adverts
@advert.get("/get_all")
async def get_advert(
    db: Session = Depends(get_db),
    params: Params = Depends(),
    current_user: User = Security(user_service.get_current_user),
):
    all_advert = Advert_service.fetch_all(db)

    data = paginate(all_advert, params)
    serialized_adverts = [serialize_advert(advert) for advert in data.items]
    # print("page-data=== ", data, Params)
    return {
        "message": "adverts retrieved successfully",
        "status_code": 200,
        "data": serialized_adverts,
        "pagination": {
            "current_page": data.page,
            "per_page": data.size,
            "total_pages": data.pages,
            "total": data.total,
        },
    }


# Get details of a specific advert.
@advert.get("/get/{advert_id}", response_model=AdvertResponse)
async def get_advert_by_id(
    advert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Security(user_service.get_current_user),
):

    advert = Advert_service.fetch(db, advert_id)
    # print(advert)
    if advert == None:
        return {"message": "advert does not exist"}
    
    return jsonable_encoder(advert)
    


# Update advert details
@advert.patch("/update/{advert_id}")
async def update_advert(
    advert_id: str,
    schema: AdvertUpdate,
    db: Session = Depends(get_db),
    #current_user: User = Security(user_service.get_current_super_admin),
):

    update_advert = Advert_service.update_advert(db, schema, advert_id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="advert updated successfully",
        data=jsonable_encoder(update_advert),
    )


# Delete specific advert.
@advert.delete("/delete/{advert_id}")
async def delete_advert(
    advert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Security(user_service.get_current_user),
):
    advert = Advert_service.delete(db, advert_id)
    if not advert:
        return {"message": "error Deleting advert"}

    return advert

    