from pydantic import BaseModel, EmailStr


class IncomingSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr
    password: str


class ReturnedSeller(BaseModel):
    id: int
    first_name: str
    last_name: str
    e_mail: EmailStr


class ReturnedSellerWithBooks(ReturnedSeller):
    books: list