from dataclasses import dataclass, field

from .types import FunctionDict


@dataclass
class Registry:
    """Simple key-value store for functions."""    
    name: str = ""  # Used for logging purposes.
    reg: FunctionDict = field(default_factory=dict)
    default_method: str = ""
    _reg_name: str = f"{name} registry" if name else "registry"

    def __getitem__(self, key: str) -> callable:
        """Get a function based on key."""
        try:
            return self.reg[key]
        except KeyError:
            raise KeyError(f"{key} not found in {self._reg_name}.")

    def __setitem__(self, key: str, value: callable):
        """Register a new function."""
        self.reg[key] = value

