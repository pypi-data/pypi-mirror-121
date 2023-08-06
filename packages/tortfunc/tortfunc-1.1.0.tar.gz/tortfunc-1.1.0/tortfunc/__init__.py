try:
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version

from .exceptions import FunctionTimeOut
from .retry import timeout_retry

__all__ = ["FunctionTimeOut", "timeout_retry"]
__version__ = version("tortfunc")
