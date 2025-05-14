from typing import Optional
from pydantic import BaseModel    



class SnellenTest(BaseModel):
    user_id: str
    eye_tested: str
    normal_acuity: int
    user_acuity: int
    visual_acuity: str
    distance: int
    