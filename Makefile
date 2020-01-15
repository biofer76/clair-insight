PWD ?= pwd_unknown
PROJECT_NAME = clair-insight
export PROJECT_NAME

cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build clair-insight Docker image
	docker build -t $(PROJECT_NAME) .

run: ## Run clair-insight Docker container
	docker run -d --env-file=.env -v $(SCAN_RESULTS_PATH):/app/data/json -v $(WHITELISTS_EXPORT_PATH):/app/data/whitelists -p $(CONTAINER_EXT_PORT):5000 --name $(PROJECT_NAME) $(PROJECT_NAME) python app.py

run-dev: ## Run clair-insight Docker container in development mode
	docker run -d --env-file=.env -v $(PWD):/app -p $(CONTAINER_EXT_PORT):5000 --name $(PROJECT_NAME) $(PROJECT_NAME) python app.py

stop: ## Stop and remove clair-insight Docker container
	docker stop $(PROJECT_NAME)
	docker rm $(PROJECT_NAME)
