from fastapi import APIRouter
from backend.app.api.v2.routers import market_overview, stream, admin, charting, news, fundamentals, analysis

api_router = APIRouter()

api_router.include_router(market_overview.router, prefix="", tags=["V2 Markets"])
api_router.include_router(charting.router, prefix="", tags=["V2 Charting"])
api_router.include_router(news.router, prefix="", tags=["V2 News"])
api_router.include_router(fundamentals.router, prefix="", tags=["V2 Fundamentals"])
api_router.include_router(analysis.router, prefix="", tags=["V2 AI Analysis"])
api_router.include_router(stream.router, prefix="", tags=["V2 Stream"])
api_router.include_router(admin.router, prefix="/admin", tags=["V2 Admin"])

