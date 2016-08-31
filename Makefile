# -*- makefile -*-
SHELL=/bin/bash
# Copyright (с) 2016.

# constants
PROJECT_NAME=Students Data base
BIND_TO=0.0.0.0
BIND_PORT=8024
MANAGE=python manage.py
DJANGO_SETTINGS_MODULE=studentsdb.settings

# TEST_APP=studentsdb,students
# TEST_OPTIONS=-v2 --keepdb

include

.PHONY: run open  clean manage help test flake8 shell ishell  migrate

run:
	@echo Starting $(PROJECT_NAME) with $(DJANGO_SETTINGS_MODULE)...
	$(MANAGE) runserver $(BIND_TO):$(BIND_PORT) --settings=$(DJANGO_SETTINGS_MODULE)

open:
	@echo Opening $(PROJECT_NAME) ...
	open 'http://$(BIND_TO):$(BIND_PORT)'

clean:
	@echo Cleaning up...
	# find ./apps/core | grep '\.pyc$$' | xargs -p -I {} rm {}
	find ./students | grep '\.pyc$$' | xargs -I {} rm {}
	find ./studentsdb | grep '\.pyc$$' | xargs -I {} rm {}
	@echo Done

manage:
ifndef cmd
	@echo Please, specify cmd=command argument to execute
else
	$(MANAGE) $(cmd) --settings=$(DJANGO_SETTINGS_MODULE)
endif

testing:
	$(MANAGE) test $(TEST_APP) $(TEST_OPTIONS)

flake:
	@echo Please, configure this command
	@echo http://flake8.pycqa.org/en/latest/
	flake8 --max-complexity 6 --exclude=migrations $(TEST_APP)

test: testing flake

pylint:
	@echo Please, specify this command in the Makefile
	@echo Please, configure this command


coverage:
	@echo Starting coverage with bash report for $(PROJECT_NAME) ...
	coverage run --source='.' --rcfile=coverage.cfg manage.py test
	coverage report

html:
	@echo Generating coverage html repot for $(PROJECT_NAME) ...
	coverage html --rcfile=coverage.cfg
	@echo Done

shell:
	# @echo Please, specify this command in the Makefile
	$(MANAGE) shell --plain

ishell:
	$(MANAGE) shell -i ipython

migrate:
ifndef app_name
	$(MANAGE) migrate
else
	@echo Starting of migration of $(app_name)
	$(MANAGE) makemigrations $(app_name)
	$(MANAGE) migrate $(app_name)
	@echo Done
endif


# SHELL := /bin/sh
LOCALPATH := ./src
PYTHONPATH := $(LOCALPATH)/
# PROJECT := someproject
PYTHON_BIN := $(VIRTUAL_ENV)/bin

showenv:
	@echo 'Environment:'
	@echo '-----------------------'
	@$(PYTHON_BIN)/python -c "import sys; print 'sys.path:', sys.path"
	@echo 'PYTHONPATH:' $(PYTHONPATH)
	@echo 'PROJECT:' $(PROJECT_NAME)
	@echo 'DJANGO_SETTINGS_MODULE:' $(DJANGO_SETTINGS_MODULE)
	@echo 'DJANGO_LOCAL_SETTINGS_MODULE:' $(DJANGO_LOCAL_SETTINGS_MODULE)
	@echo 'DJANGO_TEST_SETTINGS_MODULE:' $(DJANGO_TEST_SETTINGS_MODULE)

help:
	@cat README.md

# https://github.com/kaleissin/django-makefile/blob/master/Makefile
