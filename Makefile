PYTHON ?= python

.PHONY: install run

install:
	$(PYTHON) -m pip install -e .

run:
	taller2-pipeline
