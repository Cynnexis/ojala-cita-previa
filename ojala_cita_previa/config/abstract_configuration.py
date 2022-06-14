#!/usr/bin/env python
import abc
from typing import Union, Optional

from typeguard import typechecked


class AbstractConfiguration(abc.ABC):

	@typechecked
	def __init__(
		self,
		connect_timeout_s: Union[int, float, None] = None,
		read_timeout_s: Union[int, float, None] = None,
		sound_enabled: Optional[bool] = None,
		message_enabled: Optional[bool] = None,
		email_enabled: Optional[bool] = None,
		email_recipients: Optional[str] = None,
		email_host: Optional[str] = None,
		email_port: Optional[int] = None,
		email_username: Optional[str] = None,
		email_password: Optional[str] = None,
		email_from_email: Optional[str] = None,
		email_timeout_s: Union[int, float, None] = None,
		verbose: Optional[bool] = None,
		debug: Optional[bool] = None,
	):
		self.connect_timeout_s = connect_timeout_s
		self.read_timeout_s = read_timeout_s
		self.sound_enabled = sound_enabled
		self.message_enabled = message_enabled
		self.email_enabled = email_enabled
		self.email_recipients = email_recipients
		self.email_host = email_host
		self.email_port = email_port
		self.email_username = email_username
		self.email_password = email_password
		self.email_from_email = email_from_email
		self.email_timeout_s = email_timeout_s
		self.verbose = verbose
		self.debug = debug

	@classmethod
	@abc.abstractmethod
	def parse(cls, *args, **kwargs) -> 'AbstractConfiguration':
		raise NotImplementedError()

	def members(self) -> tuple:
		return self.connect_timeout_s, self.read_timeout_s, self.sound_enabled, self.message_enabled, self.email_enabled, self.email_recipients, self.email_host, self.email_port, self.email_username, self.email_password, self.email_from_email, self.email_timeout_s, self.verbose, self.debug

	def __eq__(self, other) -> bool:
		return isinstance(
			other, AbstractConfiguration) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return 'Configuration(' + ', '.join([
			f'connect_timeout_s: {self.connect_timeout_s}',
			f'read_timeout_s: {self.read_timeout_s}',
			f'sound_enabled: {self.sound_enabled}',
			f'message_enabled: {self.message_enabled}',
			f'email_enabled: {self.email_enabled}',
			f'email_recipients: {self.email_recipients}',
			f'email_host: {self.email_host}',
			f'email_port: {self.email_port}',
			f'email_username: {self.email_username}',
			f'email_password: {self.email_password}',
			f'email_from_email: {self.email_from_email}',
			f'email_timeout_s: {self.email_timeout_s}',
			f'verbose: {self.verbose}',
			f'debug: {self.debug}',
		]) + ')'
