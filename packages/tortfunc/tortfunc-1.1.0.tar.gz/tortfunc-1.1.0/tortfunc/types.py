try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class FunctionDict(TypedDict):
    name: str
    func: callable


class RegistryManifest(TypedDict):
    method: str
    spec: dict
