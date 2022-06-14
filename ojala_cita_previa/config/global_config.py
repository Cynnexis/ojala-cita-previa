#!/usr/bin/env python
from typing import Optional, Sequence, Any

from ojala_cita_previa.config.abstract_configuration import \
 AbstractConfiguration
from ojala_cita_previa.config.arguments import AppArguments
from ojala_cita_previa.config.file_config import FileConfig
import ojala_cita_previa.config.default_values as default_values


class GlobalConfig(AbstractConfiguration):
	"""
	Object that holds all the configuration the application should used, mixing
	the file configuration (see `FileConfig`) and the command-line arguments
	(see `AppArguments`).
	"""

	@classmethod
	def parse(
		cls,
		file_config: Optional[FileConfig] = None,
		command_line_args: Optional[AppArguments] = None,
		file_path: Optional[str] = None,
		argv: Optional[Sequence[str]] = None,
	) -> 'GlobalConfig':
		if file_config is None:
			file_config = FileConfig.parse(file_path=file_path)

		if command_line_args is None:
			command_line_args = AppArguments.parse(argv=argv)

		def d(*args) -> Optional[Any]:
			"""
			Default chain. Returns the first non-None element in the given list of arguments. If there is no such thing, returns None.
			:param args: The list if arguments.
			:return: Return the first arguments that is not None, and if not found, returns None.
			"""
			for arg in args:
				if arg is not None:
					return arg

			return None

		return GlobalConfig(
			connect_timeout_s=d(
				command_line_args.connect_timeout_s,
				file_config.connect_timeout_s,
				default_values.DEFAULT_CONNECT_TIMEOUT_S,
			),
			read_timeout_s=d(
				command_line_args.read_timeout_s,
				file_config.read_timeout_s,
				default_values.DEFAULT_READ_TIMEOUT_S,
			),
			sound_enabled=d(
				command_line_args.sound_enabled,
				file_config.sound_enabled,
				default_values.DEFAULT_SOUND_ENABLED,
			),
			message_enabled=d(
				command_line_args.message_enabled,
				file_config.message_enabled,
				default_values.DEFAULT_MESSAGE_ENABLED,
			),
			email_enabled=d(
				command_line_args.email_enabled,
				file_config.email_enabled,
				default_values.DEFAULT_EMAIL_ENABLED,
			),
			email_recipients=d(
				command_line_args.email_recipients,
				file_config.email_recipients,
				default_values.DEFAULT_EMAIL_RECIPIENTS,
			),
			email_host=d(
				command_line_args.email_host,
				file_config.email_host,
				default_values.DEFAULT_EMAIL_HOST,
			),
			email_port=d(
				command_line_args.email_port,
				file_config.email_port,
				default_values.DEFAULT_EMAIL_PORT,
			),
			email_username=d(
				command_line_args.email_username,
				file_config.email_username,
				default_values.DEFAULT_EMAIL_USERNAME,
			),
			email_password=d(
				command_line_args.email_password,
				file_config.email_password,
				default_values.DEFAULT_EMAIL_PASSWORD,
			),
			email_from_email=d(
				command_line_args.email_from_email,
				file_config.email_from_email,
				default_values.DEFAULT_EMAIL_FROM_EMAIL,
			),
			email_timeout_s=d(
				command_line_args.email_timeout_s,
				file_config.email_timeout_s,
				default_values.DEFAULT_EMAIL_TIMEOUT_S,
			),
			verbose=d(
				command_line_args.verbose,
				file_config.verbose,
				default_values.DEFAULT_VERBOSE,
			),
			debug=d(
				command_line_args.debug,
				file_config.debug,
				default_values.DEFAULT_DEBUG,
			),
		)

	def __eq__(self, other) -> bool:
		return isinstance(other,
							GlobalConfig) and self.members() == other.members()
