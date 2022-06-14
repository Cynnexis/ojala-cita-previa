#!/usr/bin/make
ifneq (,$(wildcard ./.env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif
SHELL=/bin/bash
.ONESHELL:

all: help

.PHONY: help
help:
	@echo -e "\tMakefile for ojala-cita-previa"
	@echo ''
	@echo "  usage: $0 [COMMAND]"
	@echo ''
	@echo "The available commands are:"
	@echo ''
	@echo "  help      - Print this help text and exit."
	@echo "  configure - Configure the project folder."
	@echo "  lint      - Check the code format."
	@echo "  fix-lint  - Fix the code format."
	@echo ''

.git/hooks/pre-commit:
	curl -fsSL "https://gist.githubusercontent.com/Cynnexis/cd7fdc7b911ac39b623a3a62105e7d45/raw/pre-commit" -o ".git/hooks/pre-commit"
	@if command -v "dos2unix" > /dev/null 2>&1; then \
		dos2unix ".git/hooks/pre-commit"; \
	else \
		echo "dos2unix not found. If you are on Windows, you may consider installing it."; \
	fi

.PHONY: configure-git
configure-git: .git/hooks/pre-commit

.PHONY: configure
configure: configure-git

.PHONY: clean
clean:
	find . -name '__pycache__' -type d -exec rm -rf "{}" \;
	find . -iname '*.py[co]' -type f -exec rm -f "{}" \;

.PHONY: lint
lint:
	@set -euo pipefail
	yapf -qr .

.PHONY: fix-lint
fix-lint:
	@set -euo pipefail
	yapf -ir .
