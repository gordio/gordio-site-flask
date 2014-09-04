

run:
	./venv/bin/python main.py

build:
	[ -d venv ] || virtualenv venv --no-site-packages --python=python3
	venv/bin/pip install --upgrade -r requirements.txt