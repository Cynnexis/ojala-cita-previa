#!/usr/bin/env python
import abc
from typing import Union

import beepy as beepy

from ojala_cita_previa.notification.abstract_notifier import Notifier


class SoundNotifier(Notifier):
	"""
	Notifier that emits a sound when a new change is detected.
	"""

	def __init__(self,
					success_sound: Union[str, int] = 'success',
					error_sound: Union[str, int] = 'error'):
		self.success_sound = success_sound
		self.error_sound = error_sound

	def success(self, *args, **kwargs):
		beepy.beep(sound=self.success_sound)

	def error(self, *args, **kwargs):
		beepy.beep(sound=self.error_sound)

	def members(self) -> tuple:
		return self.success_sound, self.error_sound

	def __eq__(self, other) -> bool:
		return isinstance(
			other, SoundNotifier) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return f'SoundNotifier(success_sound: {self.success_sound}, error_sound: {self.error_sound})'
