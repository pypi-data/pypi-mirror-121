from . import const as _const
import re as _re

_STRUCT = {
	'$mode': 'extend',
	'Application': [],
}

_identifier = _re.compile(r'[A-Za-z]+')

def config(mode=_const.EXTEND, *classes, **constraints):
	global _STRUCT
	newstruct = dict()

	if not mode in (_const.EXTEND, _const.STRICT):
		raise ValueError('mode must be either EXTEND or STRICT')

	_STRUCT['$mode'] = mode

	for clsname in classes:
		if not isinstance(clsname, str):
			raise TypeError(f'class names must be strings, not {type(clsname).__name__}')

		if not _identifier.fullmatch(clsname):
			raise ValueError('class names must contains only lowercase or uppercase letters')

