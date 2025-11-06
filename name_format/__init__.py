from .core import full_name

__all__ = ["full_name"]

try:
    from importlib.metadata import version

    __version__ = version("name-format")
except Exception:
    __version__ = "0.0.0"
