from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import desc
from api.db.database import get_db
from api.core.base.services import Service
from api.utils.success_response import success_response
from api.v1.models.advertisement import AdvertStatus, AdvertPriority
from api.v1.schemas import adverisements
from api.v1.models import Advert


class AdvertService(Service):
    """Advert service"""

    def create(self):
        return super().create()

    def delete(self, db: Session, Advert_id):
        Advert = db.query(Advert).filter(Advert.id == Advert_id).first()

        if not Advert:
            return {"message": "Advert does not exist"}
        else:
            delete = db.delete(Advert)
            db.commit()
            return {"message": "Advert deleted successfully", 
                    "status_code": 200}
  

    def fetch(self, db, Advert_id):
        Advert = db.query(Advert).filter(Advert.id == Advert_id).first()
        if not Advert:
            return {
                "message": "Advert not found.",
                "status_code": 404,
            }
        return Advert

    def fetch_all(self, db: Session):
        all_Adverts = db.query(Advert).all()
        return all_Adverts

    def update(self, db, schema, Advert_id):
        update_Advert = Advert_service.update_Advert(db, schema, Advert_id)
        return update_Advert

    def create_Advert(self, db: Session, schema: adverisements.AdvertCreate):

        Advert_data = schema.model_dump()

        # Convert enum fields
        if "status" in Advert_data and Advert_data["status"] is not None:
            Advert_data["status"] = AdvertStatus(Advert_data["status"])

        if "priority" in Advert_data and Advert_data["priority"] is not None:
            Advert_data["priority"] = AdvertPriority(Advert_data["priority"])

        # Create Advert schema object
        # Explicitly handle optional fields
        Advert_data = {
            k: v
            for k, v in Advert_data.items()
            if v is not None
            or k in ["description", "assigned_user_id", "required_user_role"]
        }

        # Create the Advert using the schema
        Advert = Advert(**Advert_data)

        """Creates a new Advert"""
        # Advert = Advert(**schema.dict(self))
        db.add(Advert)
        db.commit()
        db.refresh(Advert)

        return Advert

    def update_Advert(self, db: Session, schema: adverisements.AdvertUpdate, Advert_id=None):
        """Function to update a Advert"""

        Advert = db.query(Advert).filter(Advert.id == Advert_id).first()

        if not Advert:
            raise ValueError("Advert not found")

        update_data = schema.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(Advert, key, value)

        db.commit()

        db.refresh(Advert)

        return Advert

    def kol_Advert(self, db):
        kol_Adverts = db.query(Advert).filter(
            Advert.required_user_role == "KOL", Advert.status == "IN_PROGRESS"
        )
        return kol_Adverts

    def reply_Advert(self, db):
        reply_Adverts_query = db.query(Advert).filter(
            Advert.required_user_role == "Reply Guy", Advert.status == "PENDING"
        )
        return reply_Adverts_query



"""Calls Advert services"""
Advert_service = AdvertService()
