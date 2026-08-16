import os
from datetime import datetime
from config.settings import TIMEOUT_PING

def audit_node(ip):
    """Effectue un diagnostic ICMP standard sur le nœud."""
    if os.name != "nt":
        cmd = f"ping -c 1 -W {TIMEOUT_PING} {ip} > /dev/null 2>&1"
    else:
        cmd = f"ping -n 1 -w {TIMEOUT_PING * 1000} {ip} > nul"
    
    response = os.system(cmd)
    status = "En ligne" if response == 0 else "Hors ligne"
    timestamp = datetime.now().strftime("%H:%M:%S")
    return status, timestamp