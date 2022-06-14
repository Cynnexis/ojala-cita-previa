#!/usr/bin/env python
import signal
from typing import Optional, NoReturn

import bs4
import urllib3

import ojala_cita_previa as init_ojala
import ojala_cita_previa.io.network as net

from ojala_cita_previa.config.global_config import GlobalConfig
from ojala_cita_previa.notification import Notifier, get_notifier_from_args
from ojala_cita_previa.utils.stopwatch import Stopwatch

__doc__ = init_ojala.__doc__


def main(config: GlobalConfig) -> NoReturn:
	# Stopwatch that measure the time used by this script
	main_stopwatch: Stopwatch = Stopwatch(start_now=True)

	net.init()

	# Variable that indicates if the main loop should continue
	keep_looping: bool = True

	# noinspection PyUnusedLocal
	def handle_exit_signals(signum=None, frame=None) -> NoReturn:
		"""
		Callback that handles an exit signal.
		"""
		nonlocal keep_looping
		keep_looping = False
		print('Stopping program...')

	signal.signal(signal.SIGINT, handle_exit_signals)

	# Define the default timeout for all request connections
	request_timeout: urllib3.Timeout = urllib3.Timeout(
		connect=config.connect_timeout_s,
		read=config.read_timeout_s,
	)

	print('Stalking website... Press Ctrl+C to stop it.')
	try:
		last_status = None
		index_url: str = 'https://icp.administracionelectronica.gob.es/icpplus/index.html'
		notifier: Notifier = get_notifier_from_args(
			config=config, website_url=index_url)
		request_stopwatch: Stopwatch = Stopwatch(start_now=False)

		# Main loop
		while keep_looping:
			request_stopwatch.start()
			index_response: Optional[urllib3.response.HTTPResponse] = None
			try:
				index_response = net.request(index_url, timeout=request_timeout)
			except TimeoutError:
				pass
			except urllib3.exceptions.MaxRetryError:
				pass
			except urllib3.exceptions.TimeoutError:
				pass

			request_stopwatch.stop()
			if config.verbose:
				print(f'Request took {request_stopwatch.elapsed():.2f}s.')

			# Parse the response
			if index_response is None:
				if last_status is not False:
					notifier.error(
						reason=f'The request timed out ({request_stopwatch.elapsed():.2f}s).'
					)
					last_status = False
			# If success, try to parse the webpage
			elif 200 <= index_response.status < 300:
				soup = bs4.BeautifulSoup(
					index_response.data, features='html.parser')
				select_button: Optional[bs4.element.Tag] = soup.find(
					'select',
					attrs={
						'id': 'form',
						'name': 'form',
					},
				)

				# If the select button is found, send a notification
				if select_button is not None and (last_status is not True or
													last_status is None):
					notifier.success()
					last_status = True
				elif select_button is None and (last_status is True or
												last_status is None):
					notifier.error(
						reason='The dropdown-button could not be found.')
					last_status = False
			else:
				if last_status is not False:
					notifier.error(
						reason=f'The website returned the HTTP code {index_response.status}.'
					)
					last_status = False
	except KeyboardInterrupt:
		handle_exit_signals()

	net.dispose()

	main_stopwatch.stop()
	if config.verbose:
		print(f'Time elapsed: {main_stopwatch.elapsed()}s')

	print('Goodbye!')


if __name__ == '__main__':
	main(GlobalConfig.parse())
