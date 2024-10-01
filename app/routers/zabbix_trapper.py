from fastapi import APIRouter, Request, Header, HTTPException
from pydantic import BaseModel
from app.controllers.zabbix_trapper_controller import send_data_to_zabbix
from app.config import AUTH_TOKEN

# Create a router for Zabbix-related endpoints
router = APIRouter()

# Data model for the webhook payload
class WebhookData(BaseModel):
    value: str

# Webhook endpoint to receive data and send it to Zabbix
@router.post("/trapper")
async def receive_webhook(request: Request, auth: str = Header(None), webhook_data: WebhookData = None):
    if auth != AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Error no token")
    
    if webhook_data is None or not webhook_data.value:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido")

    try:
        zabbix_response = send_data_to_zabbix(webhook_data.value)
        return {"status": "success", "response": zabbix_response}
    except Exception as e:
        return {"status": "error", "message": str(e)}