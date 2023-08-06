from .structure import config
from .const import *
from .interface import apply_global, apply_local, load
from .datatypes import is_valid
	
__all__ = [
	'config', 'STRICT', 'EXTEND',
	'apply_global', 'apply_local', 'load',
	'is_valid', 'EMAIL_ADDR', 'NAME', 'FULLNAME', 'INTEGER', 'DECIMAL',
]
__doc__ = """Reading / writing configuration files"""