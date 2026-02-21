import os
import multiprocessing

from dotenv import load_dotenv
from pathlib import Path
from gunicorn.app.base import BaseApplication

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }

        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def gunicorn_config_options():
    options = {
        'bind': '0.0.0.0:8000',
        'workers': multiprocessing.cpu_count () * 2 + 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'worker_connections': 1024,
        'backlog': 2048,
        'max_requests': 5120,
        'certfile': os.getenv("gunicorn_certfile"),
        'keyfile': os.getenv("gunicorn_keyfile"),
        'accesslog': os.getenv("gunicorn_accesslog"),
        'errorlog': os.getenv("gunicorn_errorlog"),
        'daemon': True
    }
    return options


def start_gunicorn(app):
    StandaloneApplication(app, gunicorn_config_options()).run()
