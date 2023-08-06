from functools import lru_cache
from typing import Dict

from kama_sdk.utils import utils
from kama_sdk.utils.logging import lwar
from kama_sdk.model.base.model import Model


class ConfigurationPreset(Model):

  @lru_cache
  def is_default(self) -> bool:
    value = self.get_attr(IS_DEFAULT_KEY, lookback=False)
    return utils.any2bool(value)

  @lru_cache
  def variables(self) -> Dict:
    try:
      return self.get_attr(VARIABLES_KEY, depth=100)
    except:
      lwar(f"{self.get_id()} get variables raised:", True)
      return {}


VARIABLES_KEY = 'variables'
IS_DEFAULT_KEY = 'default'
