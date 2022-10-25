from fastapi import FastAPI
from presentation.route.accounts import signup

app = FastAPI()
app.include_router(signup.router)


@app.get("/api/v1/health-check")
async def health_check():
    return {"message": "alive!!!"}
