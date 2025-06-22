from .common import router as common_router
from .admin import router as admin_router
from .challenges import router as challenges_router
from .mood import router as mood_router  # Эта строка должна работать

__all__ = [
    'common_router',
    'admin_router',
    'challenges_router',
    'mood_router'
]