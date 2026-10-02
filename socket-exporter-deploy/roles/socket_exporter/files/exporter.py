#!/usr/bin/env python3
import os
import socket
import time
import threading
import sys
from prometheus_client import start_http_server, Gauge

TARGET_HOST = os.environ.get('TARGET_HOST', '127.0.0.1')
TARGET_PORT = int(os.environ.get('TARGET_PORT', '80'))
EXPORTER_PORT = int(os.environ.get('EXPORTER_PORT', '9100'))
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', '15'))

up = Gauge(
    'up', 
    'TCP Socket availability status (1=up, 0=down)', 
    ['host', 'port']
)

def check_socket():
    while True:
        try:
            with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5):
                up.labels(host=TARGET_HOST, port=TARGET_PORT).set(1)
        except (socket.timeout, ConnectionRefusedError, OSError):
            up.labels(host=TARGET_HOST, port=TARGET_PORT).set(0)
        
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    start_http_server(EXPORTER_PORT)
    checker_thread = threading.Thread(target=check_socket, daemon=True)
    checker_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)