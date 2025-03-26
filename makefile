run:
	python3 main.py

install:
	pip3 install -r requirements.txt

uninstall:
	pip3 uninstall -r requirements.txt -y

activate:
	source .venv/bin/activate

deactivate:
	deactivate

setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r requirements.txt