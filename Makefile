
PHONY: .venv
.venv: .venv/timestamp

.venv/timestamp:
	python3 -m venv .venv;
	touch .venv/timestamp

PHONY: install
install: .venv/timestamp
	.venv/bin/pip install -e .[dev]

PHONY: db
db: logger_db.sqlite3

logger_db.sqlite3: install
	.venv/bin/create_logger

PHONY: serve
serve: 
	.venv/bin/pserve development.ini --reload
