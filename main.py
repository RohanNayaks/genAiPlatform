import warnings
import uvicorn
from fastapi import FastAPI
from loguru import logger
from routers.response_router import router

warnings.filterwarnings("ignore")
logger.add("logs/app.log", rotation="500 MB", retention="7 days")

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
