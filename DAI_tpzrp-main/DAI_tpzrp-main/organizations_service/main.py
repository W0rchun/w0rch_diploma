from app.api.db import metadata, database, engine
from app.api.medins import medical_instisutions
from app.api.regions import regions
from fastapi import FastAPI
#import time

metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(medical_instisutions, prefix = '/organizations')
app.include_router(regions, prefix = '/regions')


if __name__ == "__main__":
    import uvicorn
    #time.sleep(10)
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)