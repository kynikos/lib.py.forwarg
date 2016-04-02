BASEDIR=$(CURDIR)

FORWARG=$(BASEDIR)/forwarg.py

.PHONY: help
help:
	@echo 'make test            run the tests on Python 3   '
	@echo 'make test2           run the tests on Python 2   '

.PHONY: test
test:
	cd $(BASEDIR)/test; py.test -svx

.PHONY: test2
test2:
	cd $(BASEDIR)/test; py.test2 -svx
