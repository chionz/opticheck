from typing import Optional
from pydantic import BaseModel    



class SnellenTest(BaseModel):
    normal_acuity: int
    user_acuity: int
    distance: int
    

class ColorTest(BaseModel):
    total_questions: int
    correct_answers: int
    score: Optional[bool] = None

class TumblingTest(BaseModel):
    total_questions: int
    correct_answers: int
    score: Optional[str] = None

class LeaSymbolTest(BaseModel):
    total_questions: int
    correct_answers: int
    score: Optional[str] = None
    