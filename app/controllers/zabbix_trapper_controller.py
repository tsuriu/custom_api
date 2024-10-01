from zabbix_utils import Sender
from app.config import ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_HOST, ZABBIX_ITEM_KEY
import time

# Function to send data to Zabbix
def send_data_to_zabbix(data: str):
    # Use the current time as the Unix timestamp
    timestamp = int(time.time())

    sender = Sender(server=ZABBIX_SERVER, port=ZABBIX_PORT)
    
    # Send the data value and timestamp to Zabbix
    response = sender.send_value(ZABBIX_HOST, ZABBIX_ITEM_KEY, data, timestamp)

    # Extract relevant information from the response
    return {
        "processed": response.get('processed'),
        "failed": response.get('failed'),
        "total": response.get('total'),
        "seconds_spent": response.get('seconds_spent')
    }