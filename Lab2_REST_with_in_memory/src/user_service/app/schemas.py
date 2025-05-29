from pydantic import BaseModel

class PostUser(BaseModel):
    nick: str
    fname: str
    lname: str
    password: str
    
class GetUser(BaseModel):
    nick: str
    fname: str
    lname: str

class UserLogin(BaseModel):
    nick: str
    password: str

class TakeToken(BaseModel):
    access_token: str
    token_type: str