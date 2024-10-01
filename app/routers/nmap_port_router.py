from fastapi import APIRouter, HTTPException, status, Query
from loguru import logger
from typing import Optional, Union, Dict, Any

from app.controllers.nmap_port_tests import nmap_tries

router = APIRouter()

@router.get("/")
def port_scan(
    host: Optional[str] = Query(None, description="Hostname or IP address to scan"),
    port: Optional[int] = Query(None, description="Port number to scan"),
) -> Union[Dict[str, Any], str]:
    if not host or not port:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Host and port parameters are required",
        )

    try:
        data = nmap_tries(host=host, port=port)
        if isinstance(data, dict):
            return data
        else:
            return {"message": data}  # Or handle the str return appropriately
        
    except Exception as e:
        logger.error(f"Error occurred during port scan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform port scan",
        ) from e