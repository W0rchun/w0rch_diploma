from app.api.db import metadata, database, engine
from app.api.appointments import appointments
from app.api.users import users
from fastapi import FastAPI


metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(appointments, prefix = '/appointments')
app.include_router(users, prefix = '/users')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5005, reload=True)
