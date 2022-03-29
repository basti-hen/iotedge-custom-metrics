# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
from distutils.log import error
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient
import logging
from CustomLogger import CustomLogger
import time

# initialize logger
logger = CustomLogger()


# Import Prometheus stuff
import http.server
from prometheus_client import start_http_server

# Example Visits Counter
from prometheus_client import Counter
REQUESTS = Counter('TEST_server_requests_total', 'Total number of requests to this webserver')
# Example Exceptions Counter
EXCEPTIONS = Counter('TEST_serverhandler_exceptions_total', 'Total number of exceptions raised in ServerHandler class of test.py')
# Example In Progress Gauge
from prometheus_client import Gauge
PROGRESS = Gauge('TEST_server_gauge_example', 'Number of requests in progress')

def main():
    PROGRESS.set(5)
    while True:
        logger.log(logging.ERROR, "This is an error log.")
        logger.log(logging.INFO, "This is an info log.")
        time.sleep(3600)


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # EXAMPLE EXCEPTIONS COUNTER
        EXCEPTIONS.count_exceptions()
        # EXAMPLE VISITS COUNTER
        REQUESTS.inc()
        # EXAMPLE IN PROGRESS GAUGE
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    main()
    # Start HTTP Server
    start_http_server(9600)
    server = http.server.HTTPServer(('', 9601), ServerHandler)
    logging.info("Prometheus metrics available on port 9600 /metrics")
    logging.info("HTTP server available on port 9601")
    server.serve_forever()
