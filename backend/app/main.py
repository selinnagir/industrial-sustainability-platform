from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analytics import router as analytics_router
from app.api.routes.upload import router as upload_router
from app.api.routes.company import router as company_router

app = FastAPI(
    title="Industrial Sustainability API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)
app.include_router(upload_router)
app.include_router(company_router)

@app.get("/")
def root():
    return {"message": "API is running"}
