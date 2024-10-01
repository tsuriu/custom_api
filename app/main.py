from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import http_custom_agent, nmap_port_router, zabbix_trapper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

app.include_router(http_custom_agent.router, tags=['HTTP_CUSTOM'], prefix='/api/http_custom')
app.include_router(nmap_port_router.router, tags=['NMAP_CUSTOM'], prefix='/api/nmap_custom')
app.include_router(zabbix_trapper.router, tags=['ZABBIX_TRAPPER'], prefix='/zabbix')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}