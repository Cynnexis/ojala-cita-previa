#!/usr/bin/env python
from typing import NoReturn, Optional

from ojala_cita_previa.notification.abstract_notifier import Notifier


class MessageNotifier(Notifier):
	"""
	Notifier that prints a message to the console when a new change is detected.
	"""

	def __init__(self, website_url: str):
		self.website_url = website_url

	def success(self, *args, **kwargs) -> NoReturn:
		print(f'The website {self.website_url} is online!')

	def error(self, reason: Optional[str] = None, *args, **kwargs) -> NoReturn:
		print(
			f'The website {self.website_url} is offline{f": {reason}" if reason is not None else "."}'
		)

	def members(self) -> tuple:
		return self.website_url,

	def __eq__(self, other) -> bool:
		return isinstance(
			other, MessageNotifier) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return f'MessageNotifier(website_url: {self.website_url})'
