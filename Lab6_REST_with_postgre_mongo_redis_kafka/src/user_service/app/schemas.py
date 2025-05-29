from pydantic import BaseModel


class UserEntityCreate(BaseModel):
    nick: str
    fname: str
    lname: str
    role: str
    password: str

class UserEntityRead(BaseModel):
    id: int
    nick: str
    fname: str
    lname: str
    role: str
    
    model_config = {
        "from_attributes": True,
    }
    
class UserLogin(BaseModel):
    nick: str
    password: str

class TakeToken(BaseModel):
    access_token: str
    token_type: str
