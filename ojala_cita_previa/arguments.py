#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from typing import Optional, Sequence, Union
from typeguard import typechecked

import ojala_cita_previa as init_ojala


class AppArguments:
	"""
	Class to parse and store the parameters of this application.
	"""

	DEFAULT_CONNECT_TIMEOUT_S: Union[int, float, None] = 5
	DEFAULT_READ_TIMEOUT_S: Union[int, float, None] = None

	DEFAULT_VERBOSE: bool = False
	DEFAULT_DEBUG: bool = False

	@typechecked
	def __init__(
		self,
		connect_timeout_s: Union[int, float, None] = DEFAULT_CONNECT_TIMEOUT_S,
		read_timeout_s: Union[int, float, None] = DEFAULT_READ_TIMEOUT_S,
		verbose: bool = DEFAULT_VERBOSE,
		debug: bool = DEFAULT_DEBUG,
	):
		self.connect_timeout_s = connect_timeout_s
		self.read_timeout_s = read_timeout_s
		self.verbose = verbose
		self.debug = debug

	@classmethod
	def parse(cls, argv: Optional[Sequence[str]] = None):
		"""
		Constructor for `AppArguments`. It parse the given arguments.
		:param argv: The list of arguments to parse. If not given, it will
		default to `sys.argv`
		:return: Return the corresponding instance of `AppArguments`.
		"""
		# Create main parser
		p = argparse.ArgumentParser(
			prog='ojala_cita_previa',
			description=init_ojala.__doc__,
		)

		# Declare main arguments
		p.add_argument(
			'--connect-timeout',
			'-c',
			default=cls.DEFAULT_CONNECT_TIMEOUT_S,
			help=f'The connect timeout in seconds. Defaults to {cls.DEFAULT_CONNECT_TIMEOUT_S}s.',
			type=float,
		)
		p.add_argument(
			'--read-timeout',
			'-r',
			default=cls.DEFAULT_READ_TIMEOUT_S,
			help=f'The read timeout in seconds. Defaults to {cls.DEFAULT_READ_TIMEOUT_S}s.',
			type=float,
		)
		p.add_argument(
			'--verbose',
			'-v',
			action='store_true',
			default=cls.DEFAULT_VERBOSE,
			help='Verbose mode.',
		)
		p.add_argument(
			'--debug',
			'-d',
			action='store_true',
			default=cls.DEFAULT_DEBUG,
			help='Debug mode.',
		)
		p.add_argument(
			'--version',
			'-V',
			action='version',
			version=f'%(prog)s {init_ojala.__version__}',
			help='Print the version of the script and exit.')

		args = p.parse_args(argv)

		return AppArguments(
			connect_timeout_s=args.connect_timeout,
			read_timeout_s=args.read_timeout,
			verbose=args.verbose,
			debug=args.debug,
		)

	def members(self) -> tuple:
		return self.connect_timeout_s, self.read_timeout_s, self.verbose, self.debug

	def __eq__(self, other) -> bool:
		return isinstance(other,
							AppArguments) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return f'AppArguments(connect_timeout_s: {self.connect_timeout_s}, read_timeout_s: {self.read_timeout_s}, verbose: {self.verbose}, debug: {self.debug})'
