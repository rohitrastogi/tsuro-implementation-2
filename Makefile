test:
	@pip install --quiet --requirement=requirements.txt
	py.test --verbose --color=yes
