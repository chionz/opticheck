""" User data models
"""

from sqlalchemy.dialects.postgresql import ENUM
import enum as PyEnum
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Float, text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from api.v1.models.base_model import BaseTableModel
from api.db.database import Base


genders = ENUM("male", "female", name="gender", create_type=True)


class User(BaseTableModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    wallet_address = Column(String, unique=True, nullable=True) 

    avatar_url = Column(String, nullable=True)
    is_super_admin = Column(Boolean, server_default=text("false"))
    is_deleted = Column(Boolean, server_default=text("false"))

    gender = Column(genders, nullable=True)
    age = Column(Integer, nullable=True)

    token_login = relationship(
        "TokenLogin", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    oauth = relationship(
        "OAuth", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    snellen_tests = relationship(
        "SnellenChartTest", back_populates="user", cascade="all, delete-orphan"
    )

    color_tests = relationship(
        "ColorBlindnessTest", back_populates="user", cascade="all, delete-orphan"
    )

    tumbling_tests = relationship(
        "TumblingETest", back_populates="user", cascade="all, delete-orphan"
    )


    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict.pop("password")
        return obj_dict

    def __str__(self):
        return self.email
text