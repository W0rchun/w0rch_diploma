from app.api.db import metadata, database, engine
from app.api.subdivisions import subdivisions
from app.api.doctors import doctors
from fastapi import FastAPI


metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(doctors, prefix = '/doctors')
app.include_router(subdivisions, prefix = '/subdivisions')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)