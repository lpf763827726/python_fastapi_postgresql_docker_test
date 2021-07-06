from pydantic import BaseModel, Field

## Models
class UserList(BaseModel):
    id        : str
    username  : str
    password  : str
    first_name: str
    last_name : str
    gender    : str
    create_at : str
    status    : str
class UserEntry(BaseModel):
    username  : str = Field(..., example="testUsername")
    password  : str = Field(..., example="testPassword")
    first_name: str = Field(..., example="testFirstName")
    last_name : str = Field(..., example="testLastName")
    gender    : str = Field(..., example="M")
class UserUpdate(BaseModel):
    id        : str = Field(..., example="Enter your id")
    first_name: str = Field(..., example="testFirstName")
    last_name : str = Field(..., example="testLastName")
    gender    : str = Field(..., example="M")
    status    : str = Field(..., example="1")
class UserDelete(BaseModel):
    id: str = Field(..., example="Enter your id")
