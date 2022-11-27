"""
Module define fastapi server configuration
"""

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from prometheus_client import Counter
from cpu_load_generator import load_all_cores

app = FastAPI()

REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')
HEALTHCHECK_REQUESTS = Counter('healthcheck_requests_total', 'Total number of requests to healthcheck')
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Total number of requests to main endpoint')
BYE_ENDPOINT_REQUESTS = Counter('bye_requests_total', 'Total number of requests to bye endpoint')
RISELOAD_ENDPOINT_REQUESTS = Counter('riseload_requests_total', 'Total number of requests to riseload endpoint')

class SimpleServer:
    """
    SimpleServer class define FastAPI configuration and implemented endpoints
    """

    _hypercorn_config = None

    def __init__(self):
        self._hypercorn_config = HyperCornConfig()

    async def run_server(self):
        """Starts the server with the config parameters"""
        self._hypercorn_config.bind = ['0.0.0.0:8081']
        self._hypercorn_config.keep_alive_timeout = 90
        await serve(app, self._hypercorn_config)

    @app.get("/health")
    async def health_check():
        """Implement health check endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the requests to healtcheck endpoint
        HEALTHCHECK_REQUESTS.inc()
        return {"health": "ok"}

    @app.get("/")
    async def read_main():
        """Implement main endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the total number of calls in the main endpoint
        MAIN_ENDPOINT_REQUESTS.inc()
        return {"msg": "Hello World"}

    @app.get("/bye")
    async def read_bye():
        """Implement bya endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the total number of calls in the main endpoint
        BYE_ENDPOINT_REQUESTS.inc()
        return {"msg": "Bye bye"}
    
    @app.get("/riseload")
    async def read_riseload():
        """Implement riseload endpoint"""
        # Increment counter used for register the total number of calls in the webserver
        REQUESTS.inc()
        # Increment counter used for register the total number of calls in the main endpoint
        RISELOAD_ENDPOINT_REQUESTS.inc()
        load_all_cores(duration_s=10, target_load=0.8)
        return {"msg": "Load uped"}