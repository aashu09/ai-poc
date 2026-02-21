import multiprocessing
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

name = "HIG"

accesslog = os.getenv("gunicorn_accesslog")
errorlog = os.getenv("gunicorn_errorlog")

bind = "0.0.0.0:8000"

#certfile = os.getenv("gunicorn_certfile")
#keyfile = os.getenv("gunicorn_keyfile")
# certfile = '/etc/letsencrypt/live/elladev.ecicloud.com/fullchain.pem'
# keyfile = '/etc/letsencrypt/live/elladev.ecicloud.com/privkey.pem'

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 0
keepalive = 2

debug = os.environ.get("debug", "false") == "true"
reload = False
preload_app = False
daemon = False
