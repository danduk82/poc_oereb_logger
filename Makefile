
PHONY: .venv
.venv: .venv/timestamp

.venv/timestamp:
	python3 -m venv .venv;
	touch .venv/timestamp

PHONY: install
install: .venv/timestamp
	.venv/bin/pip install -e .[dev]

PHONY: serve
serve: 
	.venv/bin/pserve development.ini --reload
