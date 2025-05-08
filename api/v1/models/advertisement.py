from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Integer, DateTime, Enum, text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from api.v1.models.base_model import BaseTableModel
from api.db.database import Base
from datetime import datetime
import enum as PyEnum

# Task status ENUM
class AdvertStatus(PyEnum.Enum):
    PENDING = "Pending"
    APPROVED = "approved"
    COMPLETED = "Completed"

# Task priority ENUM
class AdvertPriority(PyEnum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

statuses = Enum(AdvertStatus, name="advert_status", create_type=True)
priorities = Enum(AdvertPriority, name="advert_priority", create_type=True)

class Advert(BaseTableModel):
    __tablename__ = "adverts"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(statuses, default="Pending", nullable=False)
    priority = Column(priorities, default="Medium", nullable=False)
    due_date = Column(DateTime, nullable=True)

    is_deleted = Column(Boolean, server_default=text("false"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        obj_dict = super().to_dict()
        return obj_dict
