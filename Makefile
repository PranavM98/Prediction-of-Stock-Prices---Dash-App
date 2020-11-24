setup:
	python3 -m venv ~/.dashapp

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt


lint:
	pylint --disable=R,C,W1203 application.py

all: setup install lint
