import json
from typing import Dict

from flask import request

from kama_sdk.core.core import consts
from kama_sdk.utils import utils, env_utils
from kama_sdk.model.base import mc


def parse_json_body() -> Dict:
  if env_utils.is_in_cluster():
    payload_str = request.data.decode('unicode-escape')
    truncated = payload_str[1:len(payload_str) - 1]
    as_dict = json.loads(truncated)
    return utils.unmuck_primitives(as_dict)
  else:
    return utils.unmuck_primitives(request.json)


def space_id(force_single: bool, bkp_is_app=False):
  if value := request.args.get('space'):
    csv = list(map(str.strip, value.split(",")))
    return csv[0] if force_single else csv
  else:
    return consts.APP_SPACE_ID if bkp_is_app else None


def space_selector(force_single: bool, bkp_is_app=False):
  if space_or_spaces := space_id(force_single, bkp_is_app):
    return {mc.SPACE_KEY: space_or_spaces}
  else:
    return {}
