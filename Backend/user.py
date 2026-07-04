from pydantic import BaseModel
class User(BaseModel):
    session_id: str
    name_user: str
    last_name: str
    age: int