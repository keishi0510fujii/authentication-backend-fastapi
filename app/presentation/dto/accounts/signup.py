from pydantic import BaseModel, Field


class ResponseBody(BaseModel):
    id: str = Field(min_length=26, max_length=26)


class RequestBody(BaseModel):
    email: str
    password: str
    password_confirmation: str
