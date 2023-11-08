from pydantic import BaseModel

# Model Pydantic = Datatype
class Contact(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    adress: str

class ContactNoID(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    adress: str

class User(BaseModel):
    email: str
    password: str