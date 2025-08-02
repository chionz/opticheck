from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Enum, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid_extensions import uuid7
from api.db.database import Base

import enum


class TestStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class SnellenChartTest(Base):
    __tablename__ = "snellen_chart_tests"

    id = Column(String, primary_key=True, default=lambda: str(uuid7()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    eye_tested = Column(String, nullable=False)  # left, right, both
    normal_acuity = Column(Integer, default=20)
    user_acuity = Column(Integer, nullable=False)
    visual_acuity = Column(String, nullable=False)  # e.g., "20/20", "20/40"
    distance = Column(Integer, nullable=False)  # in feet
    status = Column(Enum(TestStatusEnum), default=TestStatusEnum.completed)
    tested_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="snellen_tests")


class ColorBlindnessTest(Base):
    __tablename__ = "color_blindness_tests"

    id = Column(String, primary_key=True, default=lambda: str(uuid7()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score = Column(Boolean, default=False)
    status = Column(Enum(TestStatusEnum), default=TestStatusEnum.completed)
    tested_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="color_tests")


class TumblingETest(Base):
    __tablename__ = "tumbling_e_tests"

    id = Column(String, primary_key=True, default=lambda: str(uuid7()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score = Column(String, nullable=False, server_default=text("'0%'"))
    status = Column(Enum(TestStatusEnum), default=TestStatusEnum.completed)
    tested_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tumbling_tests")

class LeaSymbolsETest(Base):
    __tablename__ = "lea_symbols_tests"

    id = Column(String, primary_key=True, default=lambda: str(uuid7()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score = Column(String, nullable=False, server_default=text("'0%'"))
    #status = Column(Enum(TestStatusEnum), default=TestStatusEnum.completed)
    tested_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="lea_symbols_tests")
