import os
from typing import Dict

import redis
from rq import Worker, Connection

from kama_sdk.cli import cli_helper
from kama_sdk.core.core import consts

redis_url = os.getenv('WORK_REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)


def get_meta() -> Dict:
  return {'name': MODE_NAME, 'info': 'Start the background worker'}


def register_arg_parser(_):
  pass


def run(options: Dict):
  cli_helper.handle_ns(options, MODE_NAME, allow_empty=False)
  _start(consts.MAIN_WORKER, consts.TELEM_WORKER)


def start_telem():
  _start(consts.TELEM_WORKER)


def _start(*queue_names: str):
  with Connection(conn):
    worker = Worker(
      queues=queue_names,
      connection=conn
    )
    worker.work()


MODE_NAME = "worker"
