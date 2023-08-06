from importlib.metadata import version
from .client import KibelaClient

try:
    __version__ = version(__name__)
except:
    pass
