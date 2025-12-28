
# Environment Management
.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: check
check:
	python -m py_compile run_clerk.py run_director.py app.py core/observability.py agents/finance.py agents/strategy.py core/container.py core/interfaces.py core/dependencies.py data/database.py services/ledger.py
	@echo "Syntax check passed!"

# Running the Assistant
.PHONY: run-clerk
run-clerk:
	python run_clerk.py --model ollama

.PHONY: run-director
run-director:
	python run_director.py --model ollama
.PHONY: app
app:
	python app.py

# Docker (Optional)
.PHONY: docker-build
docker-build:
	docker build -t finance-assistant .
