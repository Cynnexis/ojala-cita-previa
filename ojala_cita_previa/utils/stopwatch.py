#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from typing import Optional


class Stopwatch:

	def __init__(self, start_now: bool = True):
		self._begin = time.time() if start_now else -1
		self._end = -1

	def start(self):
		self._begin = time.time()
		self._end = -1

	def stop(self):
		if self._begin >= 0:
			self._end = time.time()
		return self.elapsed()

	def elapsed(self) -> Optional[float]:
		if self._begin >= 0 and self._end >= 0:
			return self._end - self._begin
		else:
			return None

	# GETTERS & SETTERS

	def get_begin(self) -> float:
		return self._begin

	def set_begin(self, begin: float) -> None:
		self._begin = begin

	begin = property(get_begin, set_begin)

	def get_end(self) -> float:
		return self._end

	def set_end(self, end: float) -> None:
		self._end = end

	end = property(get_end, set_end)

	# MAGIC FUNCTIONS

	def __call__(self, *args, **kwargs) -> Optional[float]:
		if self._begin >= 0 and self._end == -1:
			self.stop()
		else:
			self.start()
		return self.elapsed()

	def __eq__(self, o: object) -> bool:
		if isinstance(o, Stopwatch):
			return self._begin == o._begin and self._end == o._end
		else:
			return False

	def __str__(self):
		return self.elapsed()

	def __repr__(self):
		return self.elapsed()
