import argparse

from k8kat.auth.kube_broker import broker

from kama_sdk.cli import mocks_cli_entrypoint, server_cli_entrypoint, worker_cli_entrypoint, console_cli_entrypoint, \
  cli_helper
from kama_sdk.core.core import config_man_helper
from kama_sdk.model.base import static_validator
from kama_sdk.model.base.models_manager import models_manager
from kama_sdk.utils.logging import lerr

entrypoint_handlers = [
  mocks_cli_entrypoint,
  server_cli_entrypoint,
  worker_cli_entrypoint,
  console_cli_entrypoint
]


def add_sub_entrypoint(subparsers, entrypoint_module, parent):
  meta = entrypoint_module.get_meta()
  name, info = meta.get('name'), meta.get('info')
  sub_parser = subparsers.add_parser(name, help=info, parents=[parent])
  entrypoint_module.register_arg_parser(sub_parser)
  sub_parser.set_defaults(func=entrypoint_module.run)


def add_universal_args(parser: argparse.ArgumentParser):
  parser.add_argument(
    "--validate",
    default='true',
    choices=['true', 'false']
  )

  parser.add_argument(
    "-n",
    f"--{cli_helper.MOCK_NAMESPACE_FLAG}"
  )


def collect_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description='KAMA entrypoint')
  parent_parser = argparse.ArgumentParser(add_help=False)

  add_universal_args(parent_parser)

  subparsers = parser.add_subparsers()

  for entrypoint_handler in entrypoint_handlers:
    add_sub_entrypoint(subparsers, entrypoint_handler, parent_parser)

  return parser.parse_args()


def start():
  broker.connect()
  models_manager.add_defaults()
  config_man_helper.clear_trackers()
  static_validator.run_all()

  args = vars(collect_args())
  callback = args.pop('func', None)
  if callback:
    callback(args)
  else:
    lerr("unrecognized command. run --help for available commands")


MODE_MOCK = "mock"
