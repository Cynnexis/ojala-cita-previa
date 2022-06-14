#!/usr/bin/env python
from typing import Dict, Any, Type, Union, Optional

from ojala_cita_previa.config.abstract_configuration import \
 AbstractConfiguration
import ojala_cita_previa.config.default_values as default_values

import yaml


class FileConfig(AbstractConfiguration):

	@classmethod
	def parse(cls, file_path: Optional[str] = None) -> 'FileConfig':
		if file_path is None:
			file_path = default_values.DEFAULT_CONFIG_FILE_PATH

		# Define the YAML object type in Python
		yaml_object_type: Type = Dict[str, Any]

		# Read the YAML document
		with open(file_path, mode='r', encoding='utf-8') as f:
			# Parse it
			yaml_doc: yaml_object_type = yaml.load(f.read(), yaml.CLoader)

		# REQUESTS
		request: yaml_object_type = yaml_doc.get('request', {})

		connect_timeout_s: Union[int, float, None] = request.get(
			'connect_timeout_s', None)
		read_timeout_s: Union[int, float, None] = request.get(
			'read_timeout_s', None)

		# NOTIFICATIONS
		notifications: yaml_object_type = yaml_doc.get('notifications', {})

		# NOTIFICATIONS.SOUND
		sound: yaml_object_type = notifications.get('sound', {})
		sound_enabled: Optional[bool] = sound.get('enabled', None)

		# NOTIFICATIONS.MESSAGE
		message: yaml_object_type = notifications.get('message', {})
		message_enabled: Optional[bool] = message.get('enabled', None)

		# NOTIFICATIONS.EMAIL
		email: yaml_object_type = notifications.get('email', {})

		email_enabled: Optional[bool] = email.get('enabled', None)
		email_recipients: Optional[str] = email.get('recipients', None)
		email_host: Optional[str] = email.get('host', None)
		email_port: Optional[int] = email.get('port', None)
		email_username: Optional[str] = email.get('username', None)
		email_password: Optional[str] = email.get('password', None)
		email_from_email: Optional[str] = email.get('from_email', None)
		email_timeout_s: Union[int, float, None] = email.get('timeout_s', None)

		# MISC
		verbose: Optional[bool] = yaml_doc.get('verbose', None)
		debug: Optional[bool] = yaml_doc.get('debug', None)

		return FileConfig(
			connect_timeout_s=connect_timeout_s,
			read_timeout_s=read_timeout_s,
			sound_enabled=sound_enabled,
			message_enabled=message_enabled,
			email_enabled=email_enabled,
			email_recipients=email_recipients,
			email_host=email_host,
			email_port=email_port,
			email_username=email_username,
			email_password=email_password,
			email_from_email=email_from_email,
			email_timeout_s=email_timeout_s,
			verbose=verbose,
			debug=debug,
		)

	def __eq__(self, other) -> bool:
		return isinstance(other,
							FileConfig) and self.members() == other.members()
