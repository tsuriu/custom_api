import nmap3
from loguru import logger

map_port_state = {
    'open': 0,
    'closed': 1,
    'filtered': 3,
    'unfiltered': 4,
    'open|filtered': 5,
    'closed|filtered': 6
}

map_host_state = {
    'down': 0,
    'up': 1
}

def nmap_tries(host, port):
    data = None
    np = nmap3.NmapHostDiscovery()
    
    try:
        result = np.nmap_portscan_only(host, args="-p{} -Pn".format(port))
        host_dt = result[host]
        logger.info(result)
        
        data = {
            'port': {
                'port': int(host_dt['ports'][0]['portid']),
                'protocol': host_dt['ports'][0]['protocol'],
                'state': host_dt['ports'][0]['state'],
                'state_map': map_port_state[host_dt['ports'][0]['state']],
                # 'reason': host_dt['ports'][0]['reason'],
                # 'reason-ttl': int(host_dt['ports'][0]['reason_ttl'])
                },
            'state': {
                'state': host_dt['state']['state'],
                'state_map': map_host_state[host_dt['state']['state']],
                # 'reason': host_dt['state']['reason'],
                # 'reason_ttl': int(host_dt['state']['reason_ttl'])
            },
            'runtime': {
                'time': int(result['runtime']['time']),
                'elapsed': float(result['runtime']['elapsed']) * 1000,
                'exit': result['runtime']['exit']
            }
        }
        
    except Exception as e:
        data = f'{e}'
        logger.error(data)
       
    
    return data