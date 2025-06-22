from typing import Optional
from pydantic import BaseModel    



class SnellenTest(BaseModel):
    normal_acuity: int
    user_acuity: int
    distance: int
    