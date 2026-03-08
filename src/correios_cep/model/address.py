from pydantic import BaseModel, Field


class Address(BaseModel):
    state: str
    city: str
    neighborhood: str 
    zipcode: str
    street: str
