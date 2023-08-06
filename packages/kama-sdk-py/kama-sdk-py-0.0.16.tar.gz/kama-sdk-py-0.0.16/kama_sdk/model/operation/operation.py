from typing import List, Optional

from kama_sdk.core.core.types import KoD
from kama_sdk.model.action.base.action import PREFLIGHT_EVENT_TYPE, TELEM_EVENT_TYPE_KEY
from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction
from kama_sdk.model.base.mc import ATTR_KW
from kama_sdk.model.base.model import Model
from kama_sdk.model.operation.operation_state import OperationState
from kama_sdk.model.operation.step import Step
from kama_sdk.model.predicate.predicate import Predicate


class Operation(Model):

  def get_steps(self) -> List[Step]:
    """
    Loads the Steps associated with the Stage.
    :return: List of Step instances.
    """
    return self.inflate_children(Step, **{ATTR_KW: STEPS_KEY})

  def find_step_by_id(self, step_id: str) -> Step:
    """
    Finds the Step by key and inflates (instantiates) into a Step instance.
    :param step_id: identifier for desired Step.
    :return: Step instance.
    """
    matcher = lambda step: step.get_id() == step_id
    return next(filter(matcher, self.get_steps()), None)

  def get_first_step_id(self) -> Optional[str]:
    """
    Returns the key of the first associated Step, if present.
    :return: Step key or None.
    """
    if len(steps := self.get_steps()) > 0:
      return steps[0].get_id()
    return None

  def compute_next_step_id(self, crt_step: Step, op_state: OperationState) -> str:
    """
    Returns the id of the next step, or "done" if no next step exists.
    :param crt_step:
    :param op_state: if-then-else values, if necessary.
    :return: id of next step or "done".
    """
    if override_value := crt_step.compute_next_step_id(op_state):
      return override_value
    else:
      steps = self.get_steps()
      index = get_step_index(steps, crt_step.get_id())
      is_not_last = index < len(steps) - 1
      return steps[index + 1].get_id() if is_not_last else 'done'

  def get_preflight_predicate(self) -> Optional[Predicate]:
    return self.inflate_child(
      Predicate,
      attr=PREFLIGHT_PREDICATE_KEY,
      resolve_kod=False,
      safely=True
    )

  def get_preflight_action_kod(self) -> Optional[KoD]:
    if predicate := self.get_preflight_predicate():
      synth_action_kod = RunPredicatesAction.from_predicate_subclass(predicate)
      final_kod = {**synth_action_kod, **telem_patch}
      action = self.inflate_child(RunPredicatesAction, kod=final_kod)
      return action.serialize()
    else:
      return None


def get_step_index(steps: List[Step], step_id: str) -> int:
  """
  Returns the index of the desired Step.
  :param steps: list of Steps to search from.
  :param step_id: id to identify the desired Step.
  :return: index of the desired Step.
  """
  finder = (i for i, step in enumerate(steps) if step.get_id() == step_id)
  return next(finder, None)


telem_patch = {TELEM_EVENT_TYPE_KEY: PREFLIGHT_EVENT_TYPE}
STEPS_KEY = 'steps'
PREFLIGHT_PREDICATE_KEY = 'preflight_predicate'
