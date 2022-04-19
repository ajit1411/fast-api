from pydantic import BaseModel

class UserDetails(BaseModel):
    username: str
    email: str
    profile_img: str
    password: str

    class Config:
        orm_mode = True