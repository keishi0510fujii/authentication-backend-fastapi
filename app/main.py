from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/health-check")
async def health_check():
    return {"message": "alive!!!"}
