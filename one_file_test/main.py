import databases, sqlalchemy, datetime, uuid
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## Postgres Database
DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/dbtest"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id"        ,sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username"  ,sqlalchemy.String),
    sqlalchemy.Column("password"  ,sqlalchemy.String),
    sqlalchemy.Column("first_name",sqlalchemy.String),
    sqlalchemy.Column("last_name" ,sqlalchemy.String),
    sqlalchemy.Column("gender"    ,sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at" ,sqlalchemy.String),
    sqlalchemy.Column("status"    ,sqlalchemy.CHAR  ),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

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

app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="Core API",
    description="New Framework of Python",
    version="2.0",
    openapi_url="/api/v2/openapi.json",
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/users", response_model=List[UserList], tags=["Users"])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.post("/users", response_model=UserList, tags=["Users"])
async def register_user(user: UserEntry):
    gID   = str(uuid.uuid1())
    gDate = str(datetime.datetime.now())
    query = users.insert().values(
        id         = gID,
        username   = user.username,
        password   = pwd_context.hash(user.password),
        first_name = user.first_name,
        last_name  = user.last_name,
        gender     = user.gender,
        create_at  = gDate,
        status     = "1"
    )

    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at": gDate,
        "status": "1"
    }

@app.get("/users/{userId}", response_model=UserList, tags=["Users"])
async def find_user_by_id(userId: str):
    query = users.select().where(users.c.id == userId)
    return await database.fetch_one(query)

@app.put("/users", response_model=UserList, tags=["Users"])
async def update_user(user: UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name  = user.last_name,
            gender     = user.gender,
            status     = user.status,
            create_at  = gDate,
        )
    await database.execute(query)

    return await find_user_by_id(user.id)

@app.delete("/users/{userId}", tags=["Users"])
async def delete_user(user: UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This user has been deleted successfully."
    }

@app.get("/courses", tags=["Courses"])
def find_all_courses():
    return "List all courses"