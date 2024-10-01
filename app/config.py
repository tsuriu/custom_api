import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Zabbix configuration
ZABBIX_SERVER = os.getenv("ZABBIX_SERVER", "zabbix-server")
ZABBIX_PORT = int(os.getenv("ZABBIX_PORT", 10051))
ZABBIX_HOST = os.getenv("ZABBIX_HOST", "nr-server")
ZABBIX_ITEM_KEY = os.getenv("ZABBIX_ITEM_KEY", "123123")

# Authentication token
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "AgErI#ArauJo#ZBwebhook") 