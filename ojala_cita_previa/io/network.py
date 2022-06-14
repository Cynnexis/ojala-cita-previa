#!/usr/bin/env python
from typing import Optional, NoReturn, Any

import urllib3

_pool_manager: Optional[urllib3.PoolManager] = None


def init() -> urllib3.PoolManager:
	"""
	Init the pool manager. You must call this function before executing any
	network operations.
	:return: Returns the pool manager.
	:rtype: urllib3.PoolManager.
	"""
	global _pool_manager
	if _pool_manager is not None:
		_pool_manager.clear()

	_pool_manager = urllib3.PoolManager()
	return _pool_manager


def request(
	url: str,
	method: str = 'GET',
	fields: Any = None,
	headers: Any = None,
	**kwargs,
) -> urllib3.response.HTTPResponse:
	"""
	Send an HTTP request to `url` using the HTTP method `method`.

	Before performing any network operations, you need to initialize the network
	module with `init`.
	:param url: The URL to request.
	:param method: The HTTP method. Defaults to "GET".
	:param fields: Additional fields.
	:param headers: Additional HTTP headers.
	:return: The URL-LIB3 response.
	"""
	global _pool_manager
	assert _pool_manager is not None, 'Please call ojala_cita_previa.io.network.init() before performing any network operations.'
	res: urllib3.response.HTTPResponse = _pool_manager.request(
		method, url, fields=fields, headers=headers, **kwargs)

	return res


def download(
	url: str,
	method: str = 'GET',
	fields: Any = None,
	headers: Any = None,
	raise_if_not_200: bool = False,
) -> str:
	"""
	Download the content located at `url` using the HTTP method `method`.

	Before performing any network operations, you need to initialize the network
	module with `init`.
	:param url: The URL to request.
	:param method: The HTTP method. Defaults to "GET".
	:param fields: Additional fields.
	:param headers: Additional HTTP headers.
	:param raise_if_not_200: If `True`, the function will raise an `IOError` if
	the HTTP status code is not 2xx.
	:return: Return the content as a string.
	"""
	res: urllib3.response.HTTPResponse = request(
		method=method, url=url, fields=fields, headers=headers)

	if raise_if_not_200 and 200 > res.status >= 300:
		raise IOError(
			f'The request "{method} {url}" returned HTTP code {res.status}.')

	return res.data


def dispose() -> NoReturn:
	"""
	Dispose of the pool manager. This function must be called once all network
	operations are finished.
	"""
	global _pool_manager
	if _pool_manager is not None:
		_pool_manager.clear()
