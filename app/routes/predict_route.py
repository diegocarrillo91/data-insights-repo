from fastapi import APIRouter
from app.controllers.predict_controller import router as predict_routes

router = APIRouter()

router.include_router(predict_routes, prefix="/sales")


