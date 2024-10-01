from fastapi import APIRouter, HTTPException, status, Query
from loguru import logger

from app.controllers.http_custom_controller import get_website_info, get_http_req_header_details, get_certificate_info

router = APIRouter()

@router.get("/")
def req_details(url: str = Query(..., description="URL to fetch details from"), mode: str = Query("both", description="Mode of fetching details: 'http' for HTTP details only, 'cert' for certificate details only, 'both' for both")):
    try:
        if mode == 'http':
            data = get_http_req_header_details(url=url)
        elif mode == 'cert':
            hostname = url.split("//")[-1].split("/")[0]
            data = get_certificate_info(hostname)
        elif mode == 'both':
            data = get_website_info(url=url)
        else:
            raise ValueError("Invalid mode selected")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Fail to parse data',
        ) from e
    return data