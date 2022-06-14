#!/usr/bin/env python
from typing import Union, Optional

DEFAULT_CONNECT_TIMEOUT_S: Union[int, float, None] = 5
DEFAULT_READ_TIMEOUT_S: Union[int, float, None] = None

DEFAULT_SOUND_ENABLED: bool = True

DEFAULT_MESSAGE_ENABLED: bool = True

DEFAULT_EMAIL_ENABLED: bool = False
DEFAULT_EMAIL_RECIPIENTS: Optional[str] = None
DEFAULT_EMAIL_HOST: Optional[str] = None
DEFAULT_EMAIL_PORT: Optional[int] = None
DEFAULT_EMAIL_USERNAME: Optional[str] = None
DEFAULT_EMAIL_PASSWORD: Optional[str] = None
DEFAULT_EMAIL_FROM_EMAIL: Optional[str] = None
DEFAULT_EMAIL_TIMEOUT_S: Union[int, float, None] = 5

DEFAULT_VERBOSE: bool = False
DEFAULT_DEBUG: bool = False

DEFAULT_CONFIG_FILE_PATH: str = 'ojala.yml'
