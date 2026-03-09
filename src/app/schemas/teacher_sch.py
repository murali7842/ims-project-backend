from pydantic import EmailStr, BaseModel



class CreateTeacherSch(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone_number:str
    address:str
    institution_id: int