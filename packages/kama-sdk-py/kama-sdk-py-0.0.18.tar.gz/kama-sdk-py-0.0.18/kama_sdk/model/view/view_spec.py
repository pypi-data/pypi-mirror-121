from typing import Dict

from kama_sdk.model.base.model import Model


class ViewSpec(Model):

  def compute_spec(self) -> Dict:
    return self.get_attr(SPEC_KEY, depth=100)


SPEC_KEY = "spec"
