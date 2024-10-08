import ssl
import socket
import datetime
import pycurl
import re
from loguru import logger

def get_certificate_info(hostname, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName'] # type: ignore
        issuer = dict(x[0] for x in cert['issuer']) # type: ignore
        issued_by = issuer['commonName']
        valid_from = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        valid_to = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z') # type: ignore
        serial_number = cert['serialNumber']
        time_to_expire = valid_to - datetime.datetime.utcnow()

        cert_info = {
            'Issued To': issued_to,
            'Issued By': issued_by,
            'Valid From': valid_from,
            'Valid To': valid_to,
            'Serial Number': serial_number,
            'Time to Expire': time_to_expire.total_seconds()
        }

    except Exception as e:
        logger.error(str(e))
        cert_info = {
            'Issued To': None,
            'Issued By': None,
            'Valid From': None,
            'Valid To': None,
            'Serial Number': None,
            'Time to Expire': None,
            'error': str(e)
        }

    return cert_info


def get_http_req_header_details(url):
    try:
        c = pycurl.Curl()

        c.setopt(pycurl.URL, url)  # Set URL
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.WRITEFUNCTION, lambda bytes: len(bytes))

        # Check if the URL is using HTTPS, if so, ignore SSL verification
        if 'https' in url:
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)

        c.perform()  # Execute request
        
        # Get required details
        status_code = c.getinfo(pycurl.HTTP_CODE)
        dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME)  # DNS lookup time
        conn_time = c.getinfo(pycurl.CONNECT_TIME)    # TCP/IP handshake time
        starttransfer_time = c.getinfo(pycurl.STARTTRANSFER_TIME)  # Time to first byte
        total_time = c.getinfo(pycurl.TOTAL_TIME)  # Total request time
        
        c.close()

        # Store the details in a dictionary
        http_info = {
            'dns_time': dns_time,
            'status_code': status_code,
            'conn_time': conn_time,
            'starttransfer_time': starttransfer_time,
            'total_time': total_time
        }
        
    except pycurl.error as e:
        error_message = f'{e}'
        matches = re.findall(r"\((.*?)\)", error_message)
        match_details = matches[0].split(',') if matches else ['0', 'Unknown error']
        
        logger.error(error_message)
        
        # Store error details in case of an exception
        http_info = {
            'dns_time': 0,
            'conn_time': 0,
            'starttransfer_time': 0,
            'total_time': 0,
            'status_code': 10000,
            'error': {'type': int(match_details[0]), 'descr': match_details[1].strip()} 
        }

    return http_info


def get_website_info(url):
    hostname = url.split("//")[-1].split("/")[0]
    cert_info = get_certificate_info(hostname)
    http_info = get_http_req_header_details(url)
    
    combined_info = {
        'certificate_info': cert_info,
        'http_info': http_info
    }
    
    return combined_info