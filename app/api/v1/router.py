from fastapi import APIRouter

from app.api.v1 import (
    admin,
    auth,
    community,
    contact,
    destinations,
    enquiries,
    events,
    hidden_india,
    stories,
    trips,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(destinations.router)
api_router.include_router(trips.router)
api_router.include_router(events.router)
api_router.include_router(hidden_india.router)
api_router.include_router(stories.router)
api_router.include_router(community.router)
api_router.include_router(enquiries.router)
api_router.include_router(contact.router)
api_router.include_router(auth.router)
api_router.include_router(auth.admin_auth_router)
api_router.include_router(admin.router)
