#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Oh no! I can't get my cita previa online because the Spanish government website crashed again! Don't worry, "Ojalá Cita Previa" got your back! It will notify you when the website is back online, so you can be one of the first to get your cita.
"""
from typing import Union

MAJOR: Union[int, str] = 0
MINOR: Union[int, str] = 0
PATCH: Union[int, str] = 1
DEV: Union[int, str, None] = None

__version__: str = f'{MAJOR}.{MINOR}.{PATCH}'
if DEV is not None:
	__version__ += f'.dev{DEV}'
