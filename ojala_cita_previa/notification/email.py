#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import ssl
from typing import Union, List, Optional, NoReturn

from ojala_cita_previa.notification.abstract_notifier import Notifier


class EmailNotifier(Notifier):

	def __init__(
		self,
		website_url: str,
		recipients: Union[List[str], str],
		host: str,
		port: int,
		username: str,
		password: str,
		from_email: Optional[str] = None,
		timeout_s: int = 10,
	):
		self.website_url = website_url
		self.recipients = recipients
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.from_email = from_email
		self.timeout_s = timeout_s

	@staticmethod
	def send_email(
		subject: str,
		content: str,
		recipients: Union[List[str], str],
		host: str,
		port: int,
		username: str,
		password: str,
		from_email: Optional[str] = None,
		timeout_s: int = 5,
	) -> NoReturn:
		"""
		Send an email using SMTP.
		:param subject: The subject of the email. It will be sent in UTF-8.
		:param content: The content of the email. It will be sent in UTF-8.
		:param recipients: The recipients of the email. It can be a string of comma-separated email addresses, or a list of string.
		:param host: The host of the server.
		:param port: The SMTP port of the server.
		:param username: The username to login to the SMTP server.
		:param password: The password to login to the SMTP server.
		:param from_email: The "From" field of the server. Defaults to "username".
		:param timeout_s: The timeout, in seconds. Default to 5s.
		"""
		if from_email is None:
			from_email = username

		if isinstance(recipients, str):
			recipients = [recipients]

		recipients: List[str]

		# create message
		msg = MIMEText(content, 'plain', 'utf-8')
		msg['Subject'] = Header(subject, 'utf-8')
		msg['From'] = from_email
		msg['To'] = ', '.join(recipients)

		# send it via SMTP
		context = ssl.create_default_context()

		try:
			with smtplib.SMTP(
				host=host, port=port, timeout=timeout_s) as server:
				server.ehlo()
				server.starttls(context=context)
				server.ehlo()
				server.login(username, password)
				failed_recipients: Optional[dict] = server.sendmail(
					from_addr=msg['From'],
					to_addrs=msg['To'],
					msg=msg.as_string())

			if len(failed_recipients) > 0:
				print(
					f'The following recipients could not be reached:\n{json.dumps(failed_recipients, indent=2)}',
					file=sys.stderr)
		except smtplib.SMTPException as e:
			print(f'The following exception was caught:\n{e}', file=sys.stderr)
		except TimeoutError as e:
			print(
				f'Could not send the email because of the timeout:\n{e}',
				file=sys.stderr)

	def success(self, *args, **kwargs) -> NoReturn:
		self.send_email(
			subject='[Ojala Cita Previa] Website is online!',
			content=f'The website {self.website_url} is online!',
			recipients=self.recipients,
			host=self.host,
			port=self.port,
			username=self.username,
			password=self.password,
			from_email=self.from_email,
			timeout_s=self.timeout_s,
		)

	def error(self, reason: Optional[str] = None, *args, **kwargs) -> NoReturn:
		self.send_email(
			subject='[Ojala Cita Previa] Website is offline',
			content=f'The website {self.website_url} is offline{f": {reason}" if reason is not None else "."}',
			recipients=self.recipients,
			host=self.host,
			port=self.port,
			username=self.username,
			password=self.password,
			from_email=self.from_email,
			timeout_s=self.timeout_s,
		)

	def members(self) -> tuple:
		return self.website_url, self.recipients, self.host, self.port, self.username, self.password, self.from_email, self.timeout_s

	def __eq__(self, other) -> bool:
		return isinstance(
			other, EmailNotifier) and self.members() == other.members()

	def __hash__(self) -> int:
		return hash(self.members())

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return 'MessageNotifier(' + ', '.join([
			f'website_url: {self.website_url}'
			f'recipients: {self.recipients}'
			f'host: {self.host}'
			f'port: {self.port}'
			f'username: {self.username}'
			f'password: {self.password}'
			f'from_email: {self.from_email}'
			f'timeout_s: {self.timeout_s}'
		]) + ')'
