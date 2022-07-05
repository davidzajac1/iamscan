target:
	$(info ${HELP_MESSAGE})
	@exit 0

test:
	python -m pytest tests/test_code.py

test-one:
	python -m iamscan -p tests/py/awsec2instances.py

black:
	black setup.py iamscan/* tests/test_code.py tests/validations.py

black-check:
	black --check setup.py iamscan/* tests/test_code.py tests/validations.py

define HELP_MESSAGE

Usage: $ make [TARGETS]

TARGETS
	test        	Run the Unit tests.
	test-one		Run for just one file.
	black			Format all Python files.
	black-check 	Check if Python files are formatted.
	
endef