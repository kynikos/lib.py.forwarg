BASEDIR=$(CURDIR)

FORWARG=$(BASEDIR)/forwarg.py

.PHONY: help
help:
	@echo 'make test            run the tests               '

.PHONY: test
test:
	cd $(BASEDIR)/test; py.test -svx