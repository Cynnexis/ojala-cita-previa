#!/usr/bin/env python
from typing import List, Optional

from ojala_cita_previa.notification.email import EmailNotifier
from ojala_cita_previa.notification.message import MessageNotifier
from ojala_cita_previa.notification.sound import SoundNotifier
from ojala_cita_previa.notification.broadcast_notifier import BroadcastNotifier
from ojala_cita_previa.config.global_config import GlobalConfig as _GlobalConfig
from ojala_cita_previa.notification.abstract_notifier import Notifier


def get_notifier_from_args(
	config: _GlobalConfig,
	website_url: str,
) -> Optional[Notifier]:
	"""
	Return the notifier the application should used based on the configuration.
	:param config: The configuration.
	:param website_url: The URL of the website to inspect.
	:return: Returns a Notifier, or None if the configuration specify no
	notifiers.
	"""
	notifiers: List[Notifier] = []

	if config.sound_enabled:
		notifiers.append(SoundNotifier())

	if config.message_enabled:
		notifiers.append(MessageNotifier(website_url=website_url))

	if config.email_enabled:
		notifiers.append(
			EmailNotifier(
				website_url=website_url,
				recipients=config.email_recipients,
				host=config.email_host,
				port=config.email_port,
				username=config.email_username,
				password=config.email_password,
				from_email=config.email_from_email,
				timeout_s=config.email_timeout_s,
			),)

	if len(notifiers) == 0:
		return None
	elif len(notifiers) == 1:
		return notifiers[0]
	else:
		return BroadcastNotifier(notifiers=notifiers)
