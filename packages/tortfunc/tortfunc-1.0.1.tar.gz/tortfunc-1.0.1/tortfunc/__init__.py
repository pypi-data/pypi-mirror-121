try:
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version

from .exceptions import FunctionTimeOut
from .retry import retry_function

__all__ = ["FunctionTimeOut", "retry_function"]
__version__ = version("tortfunc")
