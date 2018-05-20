.PHONY: test

test:
	@pip install --quiet --requirement=requirements.txt
	cd test; python -m pytest --verbose --color=yes
