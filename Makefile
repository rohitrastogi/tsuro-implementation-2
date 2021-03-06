.PHONY: test
setup:
	@pip install --requirement=requirements.txt	

test:
	@pip install --quiet --requirement=requirements.txt
	cd test; python -m pytest --verbose --color=yes

tournament:
	@pip install --quiet --requirement=requirements.txt
	cd src; python tournament.py
