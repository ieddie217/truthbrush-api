from fastapi import APIRouter, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from ...services.truthbrush_service import TruthbrushService
from ...core.auth import verify_basic_auth

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/statuses")
def get_statuses(
    username: str = Query(..., description="Truth Social username"),
    created_after: Optional[str] = Query(None, description="ISO date/time string, e.g. 2025-07-23 or 2025-07-23T00:00:00"),
    replies: bool = Query(False, description="Include replies? (default: False)"),
    pinned: bool = Query(False, description="Only pinned posts? (default: False)"),
    request: Request = None,
    auth_user: str = Depends(verify_basic_auth),
):
    """
    Returns statuses for a given username, optionally filtered by created_after (ISO date string).
    Output is a JSON array, each item matching the structure of data.json.
    Requires HTTP Basic Authentication.
    """
    # Log the request
    client_ip = request.client.host if request else 'unknown'
    logger.info(f"/statuses called from {client_ip} by user {auth_user} with username={username}, created_after={created_after}, replies={replies}, pinned={pinned}")
    
    # Initialize service and get data
    try:
        service = TruthbrushService()
        statuses = service.get_user_statuses(
            username=username,
            created_after=created_after,
            replies=replies,
            pinned=pinned
        )
        return JSONResponse(content=statuses)
    except ValueError as e:
        # Bad request - invalid parameters
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Internal server error
        logger.error(f"Unexpected error in /statuses endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 