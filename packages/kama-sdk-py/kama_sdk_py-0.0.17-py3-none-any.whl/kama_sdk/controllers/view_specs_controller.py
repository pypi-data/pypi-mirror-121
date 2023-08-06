import base64
import json
from importlib import import_module
from typing import Dict, Type, Optional

from flask import Blueprint, jsonify, request

from kama_sdk.model.base.mc import FULL_SEARCHABLE_KEY
from kama_sdk.model.view.grid_view_spec import GridViewSpec
from kama_sdk.model.view.table_view_spec import TableViewSpec
from kama_sdk.model.view.view_spec import ViewSpec
from kama_sdk.serializers.view_spec_ser import ser_grid_minimal_meta
from kama_sdk.utils.logging import lwar, lerr
from kama_sdk.utils.utils import snake2camel

controller = Blueprint('view_specs_controller', __name__)

BASE_PATH = '/api/view_specs'


@controller.route(BASE_PATH)
def get_index():
  classes = [GridViewSpec, TableViewSpec]
  query = {FULL_SEARCHABLE_KEY: True}
  models = []
  for cls in classes:
    class_models = cls.inflate_all(q=query)
    models.extend(class_models)
  return jsonify(data=list(map(ser_grid_minimal_meta, models)))


@controller.route(f'{BASE_PATH}/<spec_type>/<spec_id>/meta')
def get_view_meta(spec_type: str, spec_id):
  if spec_class := load_view_spec_cls(spec_type):
    if spec_model := spec_class.inflate(spec_id, patch=compute_patch()):
      meta = spec_model.compute_spec()
      return jsonify(data=meta)
    else:
      return jsonify({'error': f"no such {spec_type} '{spec_id}'"}), 400
  else:
    return jsonify({'error': f"no such view type '{spec_id}'"}), 400


@controller.route(f'{BASE_PATH}/<spec_type>/<spec_id>/compute')
def get_view_data(spec_type: str, spec_id):
  if spec_class := load_view_spec_cls(spec_type):
    if spec_model := spec_class.inflate(spec_id, patch=compute_patch()):
      if isinstance(spec_model, TableViewSpec):
        data = spec_model.compute_frame_view_specs()
        return jsonify(data=data)
      else:
        return jsonify({'error': f"non-table {spec_type} '{spec_id}'"}), 400
    else:
      return jsonify({'error': f"no such {spec_type} '{spec_id}'"}), 400
  else:
    return jsonify({'error': f"no such view type '{spec_id}'"}), 400


@controller.route(f'{BASE_PATH}/<grid_type>/<grid_id>/cells/<cell_id>/compute')
def get_collection_cell_data(grid_type, grid_id, cell_id):
  if spec_class := load_grid_spec_cls(grid_type):
    if grid := spec_class.inflate(grid_id, patch=compute_patch()):
      data = grid.compute_cell_view_spec(cell_id)
      return jsonify(data=data)
    else:
      return jsonify({'error': f"no such set {grid_id}"}), 400
  else:
    return jsonify({'error': f"no such view type '{grid_id}'"}), 400


def compute_patch() -> Dict:
  if b64_enc_str := request.args.get('b64_enc_data'):
    try:
      utc_str = base64.b64decode(b64_enc_str)
      return json.loads(utc_str)
    except Exception as e:
      lwar(f"failed to decode b64 data", exc=e)
      return {}
  else:
    return {}


def load_grid_spec_cls(view_type_plural: str) -> Optional[Type[GridViewSpec]]:
  return load_view_spec_cls(view_type_plural)


def load_view_spec_cls(view_type_plural: str) -> Optional[Type[ViewSpec]]:
  try:
    singular = view_type_plural[:-1]
    mod_name = f"kama_sdk.model.view.{singular}_view_spec"
    class_name = f"{snake2camel(singular)}ViewSpec"
    module = import_module(mod_name)
    return getattr(module, class_name)
  except Exception as e:
    lerr(f"failed to load spec cls for {view_type_plural}", exc=e)
    return None
