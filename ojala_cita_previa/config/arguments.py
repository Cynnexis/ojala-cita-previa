#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from typing import Optional, Sequence

import ojala_cita_previa as init_ojala
from ojala_cita_previa.config.abstract_configuration import \
 AbstractConfiguration
import ojala_cita_previa.config.default_values as default_values


class AppArguments(AbstractConfiguration):
	"""
	Class to parse and store the parameters of this application.
	"""

	@classmethod
	def parse(cls, argv: Optional[Sequence[str]] = None) -> 'AppArguments':
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
			default=None,
			help=f'The connect timeout in seconds. Defaults to {default_values.DEFAULT_CONNECT_TIMEOUT_S}s.',
			type=float,
		)
		p.add_argument(
			'--read-timeout',
			'-r',
			default=None,
			help=f'The read timeout in seconds. Defaults to {default_values.DEFAULT_READ_TIMEOUT_S}s.',
		)
		p.add_argument(
			'--no-sound',
			action='store_true',
			default=None,
			help=f'Disable the sound. Defaults to {not default_values.DEFAULT_SOUND_ENABLED}.',
		)
		p.add_argument(
			'--no-message',
			action='store_true',
			default=None,
			help=f'Disable the output on the terminal. Defaults to {not default_values.DEFAULT_MESSAGE_ENABLED}.',
		)
		p.add_argument(
			'--email-recipients',
			default=None,
			help=f'The list of recipients (comma-separated) to send to to notify of a change. Defaults to {default_values.DEFAULT_EMAIL_RECIPIENTS}',
		)
		p.add_argument(
			'--email-host',
			default=None,
			help=f'The email host server. Defaults to {default_values.DEFAULT_EMAIL_HOST}',
		)
		p.add_argument(
			'--email-port',
			default=None,
			help=f'The email SMTP port to connect to the server. Defaults to {default_values.DEFAULT_EMAIL_PORT}',
		)
		p.add_argument(
			'--email-username',
			default=None,
			help=f'The username to use to log in to the SMTP server. Defaults to {default_values.DEFAULT_EMAIL_USERNAME}',
		)
		p.add_argument(
			'--email-password',
			default=None,
			help=f'The password to use to log in to the SMTP server. Defaults to {default_values.DEFAULT_EMAIL_PASSWORD}',
		)
		p.add_argument(
			'--email-from-email',
			default=None,
			help=f'The "From" field for the email. Defaults to {default_values.DEFAULT_EMAIL_FROM_EMAIL}',
		)
		p.add_argument(
			'--email-timeout',
			default=None,
			help=f'The email sending timeout. Defaults to {default_values.DEFAULT_EMAIL_TIMEOUT_S}s',
		)
		p.add_argument(
			'--verbose',
			'-v',
			action='store_true',
			default=None,
			help='Verbose mode.',
		)
		p.add_argument(
			'--debug',
			'-d',
			action='store_true',
			default=None,
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
			connect_timeout_s=float(args.connect_timeout) if isinstance(
				args.connect_timeout, str) else args.connect_timeout,
			read_timeout_s=float(args.read_timeout) if isinstance(
				args.read_timeout, str) else args.read_timeout,
			sound_enabled=args.no_sound,
			message_enabled=args.no_message,
			email_enabled=None,
			email_recipients=args.email_recipients,
			email_host=args.email_host,
			email_port=int(args.email_port)
			if isinstance(args.email_port, str) else args.email_port,
			email_username=args.email_username,
			email_password=args.email_password,
			email_from_email=args.email_from_email,
			email_timeout_s=float(args.email_timeout) if isinstance(
				args.email_timeout, str) else args.email_timeout,
			verbose=args.verbose,
			debug=args.debug,
		)

	def __eq__(self, other) -> bool:
		return isinstance(other,
							AppArguments) and self.members() == other.members()
