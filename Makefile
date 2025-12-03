BLACK=black
PYTHON= ?= python3

.PHONY : \
	check \
	all \
	install \
	clean \
	check-format \
	format

all: check-format check

install:
	pipx install .

check:
	$(MAKE) -C tests check

check-format:
	$(BLACK) --version
	$(BLACK) --check templateprocessor
	$(BLACK) --check tests

format:
	$(BLACK) templateprocessor
	$(BLACK) tests

clean:
	rm -r -f build