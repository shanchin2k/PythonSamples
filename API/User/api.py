from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

API_KEY = "12345ABCDEF"

@app.middleware("http")
async def api_key_middleware(request, call_next):
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    return await call_next(request)

@app.get("/welcome")
def welcome():
    return {"message": "Welcome to my API"}

@app.get("/user")
def user_profile():
    return {
        "name": "Test",
        "email": "test@test.com",
        "website": "www.test.com",
        "linkedin": "https://www.linkedin.com/in/test"
    }

@app.get("/user/{userId}")
def user_profile(userId: int):
    if userId == 1:
        return {
            "name": "Test",
            "email": "test@test.com",
            "website": "www.test.com",
            "linkedin": "https://www.linkedin.com/in/test"
        }
    else:
        return {
            "name": "Exception",
            "email": "exception@test.com",
            "website": "www.exception.com",
            "linkedin": "https://www.linkedin.com/in/exception"
        }


class User(BaseModel):
    name: str
    age: int
    email: str

users = []
@app.post("/users")
def new_user(user: User):
    users.append(user.model_dump())
    return {"message": "User created successfully", "Total users": len(users)}



