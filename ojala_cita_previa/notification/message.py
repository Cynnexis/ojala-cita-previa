#!/usr/bin/env python
from typing import NoReturn, Optional


def success(url: str) -> NoReturn:
	print(f'The website {url} is online!')


def error(url: str, reason: Optional[str] = None) -> NoReturn:
	print(
		f'The website {url} is offline{f": {reason}" if reason is not None else "."}'
	)
