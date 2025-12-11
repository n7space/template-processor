SRC_DIR = ../../
PYTHON ?= python3

TESTS = \
	test_ivreader.py \
	test_dvreader.py \
	test_soreader.py \
	test_templateinstantiator.py \
	test_md2docx.py

.PHONY: \
	check

check: ${TESTS}
	PYTHONPATH=${SRC_DIR} ${PYTHON} -m pytest ${TESTS} -vv