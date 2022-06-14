#!/usr/bin/env python
from typing import Optional

import ojala_cita_previa as init_ojala
import ojala_cita_previa.io.network as net
import ojala_cita_previa.notification.message as message
import ojala_cita_previa.notification.sound as sound

import urllib3
import bs4

__doc__ = init_ojala.__doc__

from ojala_cita_previa.arguments import AppArguments
from ojala_cita_previa.utils.stopwatch import Stopwatch


def main(args: AppArguments):
	net.init()

	# Define the default timeout for all request connections
	request_timeout: urllib3.Timeout = urllib3.Timeout(
		connect=args.connect_timeout_s,
		read=args.read_timeout_s,
	)

	print('Stalking website... Press Ctrl+C to stop it.')
	try:
		last_status = None
		index_url: str = 'https://icp.administracionelectronica.gob.es/icpplus/index.html'
		while True:
			request_stopwatch: Stopwatch = Stopwatch(start_now=True)
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
			if args.verbose:
				print(f'Request took {request_stopwatch.elapsed():.2f}s.')

			# Parse the response
			if index_response is None:
				if last_status is not False:
					message.error(
						index_url,
						f'The request timed out ({request_stopwatch.elapsed():.2f}s).'
					)
					sound.error()
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
					message.success(index_url)
					sound.success()
					last_status = True
				elif select_button is None and (last_status is True or
												last_status is None):
					message.error(index_url,
									'The dropdown-button could not be found.')
					sound.error()
					last_status = False
			else:
				if last_status is not False:
					message.error(
						index_url,
						f'The website returned the HTTP code {index_response.status}.'
					)
					sound.error()
					last_status = False
	except KeyboardInterrupt:
		print('Stopping program...')

	net.dispose()
	print('Goodbye!')


if __name__ == '__main__':
	main(AppArguments.parse())
