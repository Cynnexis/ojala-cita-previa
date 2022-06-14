#!/usr/bin/env python
import abc
from typing import NoReturn


class Notifier(abc.ABC):
	"""
	Abstract class for a notifier.
	"""

	@abc.abstractmethod
	def success(self, *args, **kwargs) -> NoReturn:
		raise NotImplementedError()

	@abc.abstractmethod
	def error(self, *args, **kwargs) -> NoReturn:
		raise NotImplementedError()

	@abc.abstractmethod
	def members(self) -> tuple:
		raise NotImplementedError()

	def __eq__(self, other) -> bool:
		return isinstance(other, Notifier) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return 'Notifier()'
