from pydantic import BaseModel

class Player(BaseModel):
    id: str
    name: str