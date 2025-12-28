
# Personal Finance Assistant Makefile

PYTHON := ./.venv/bin/python
PIP := ./.venv/bin/pip
VENV := .venv
UVICORN := ./.venv/bin/uvicorn
MLFLOW := ./.venv/bin/mlflow

.PHONY: help install run-ui run-clerk run-director test evaluate mlflow-ui clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

$(VENV): ## Create virtual environment if it does not exist
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: $(VENV) ## Install dependencies in virtual environment
	$(PIP) install -r requirements.txt

run-ui: ## Start the Web UI (FastAPI/PydanticAI)
	./start_ui.sh

run-clerk: ## Run Finance Clerk CLI (Expense Tracking)
	$(PYTHON) run_clerk.py

run-director: ## Run Wealth Director CLI (Strategy)
	$(PYTHON) run_director.py

test: ## Run strict E2E tests
	$(PYTHON) tests/e2e_test.py

evaluate: ## Run MLflow evaluation suite
	$(PYTHON) tests/evaluate_agents.py

mlflow-ui: ## Start MLflow Dashboard
	$(MLFLOW) ui

clean: ## Remove python cache and artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
