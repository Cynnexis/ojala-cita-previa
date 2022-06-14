#!/usr/bin/env python
import beepy as beepy


def success():
	beepy.beep(sound='success')


def error():
	beepy.beep(sound='error')
