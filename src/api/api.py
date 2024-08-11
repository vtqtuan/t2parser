from fastapi import APIRouter

from src.api.routes import parser

router = APIRouter()
router.include_router(parser.router, tags=["parser"], prefix="/parse")