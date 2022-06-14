#!/usr/bin/env python
from typing import List, Union, NoReturn

from ojala_cita_previa.notification.abstract_notifier import Notifier


class BroadcastNotifier(Notifier):
	"""
	Notifier that contains a sequence of notifiers, to call when a changes as
	been detected.
	"""

	def __init__(self, notifiers: Union[Notifier, List[Notifier]]):
		self.notifiers = []
		if isinstance(notifiers, list):
			self.notifiers = notifiers
		else:
			self.notifiers = [notifiers]

	def success(self, *args, **kwargs) -> NoReturn:
		for notifier in self.notifiers:
			notifier.success(*args, **kwargs)

	def error(self, *args, **kwargs) -> NoReturn:
		for notifier in self.notifiers:
			notifier.error(*args, **kwargs)

	def members(self) -> tuple:
		return self.notifiers,

	def __eq__(self, other) -> bool:
		return isinstance(
			other, BroadcastNotifier) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return f'BroadcastNotifier(notifiers: {self.notifiers})'
