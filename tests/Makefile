SRC_DIR = ../../
PYTHON ?= python3

TESTS = \
	test_ivreader.py

.PHONY: \
	check

check: ${TESTS}
	PYTHONPATH=${SRC_DIR} ${PYTHON} -m pytest ${TESTS} -vv