# --- Wealth OS Makefile ---

# Configuration
PYTHON = python3
PIP = pip3
STREAMLIT = streamlit
APP_ENTRY = streamlit_app.py

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "Wealth OS Terminal - Development Command Suite"
	@echo "==============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Environment ---

.PHONY: install
install: ## Install project dependencies
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

.PHONY: clean
clean: ## Remove temporary build and cache artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	rm -rf .mlflow
	@echo "Cleanup complete."

# --- Running ---

.PHONY: ui
ui: ## Launch the Wealth OS Streamlit Terminal
	$(STREAMLIT) run $(APP_ENTRY)

.PHONY: clerk
clerk: ## Run the CLI Clerk Agent (Ollama)
	$(PYTHON) run_clerk.py --model ollama

.PHONY: director
director: ## Run the CLI Director Agent (Ollama)
	$(PYTHON) run_director.py --model ollama

# --- Observability & QA ---

.PHONY: mlflow
mlflow: ## Launch MLflow Tracking UI
	mlflow ui --port 5001

.PHONY: test
test: ## Run suite of unit and strategy tests
	pytest tests/

.PHONY: lint
lint: ## Run syntax and static analysis audit
	$(PYTHON) -m py_compile $(APP_ENTRY) run_clerk.py run_director.py core/*.py finance/*.py
	@echo "Audit passed."

# --- Deployment ---

.PHONY: docker-build
docker-build: ## Build the institutional docker container
	docker build -t wealth-os-terminal .
