.PHONY: help

.DEFAULT_GOAL := help

RUN_LIKE_USER = run --rm -u `id -u`:`id -g` web
COMPOSE_COMMAND = docker-compose -f dev.yml


help: ## This help.
	@echo
	@echo "\e[1;35m Port mapping used: $<\e[0m"
	@echo "\e[1;33m - Backend: localhost:8000 $<\e[0m"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo


build:
	$(COMPOSE_COMMAND) build

up:
	$(COMPOSE_COMMAND) up

upd: ## Run developer containers without print messages.
	$(COMPOSE_COMMAND) up -d

createsuperuser: ## Create superuser.
	$(COMPOSE_COMMAND) $(RUN_LIKE_USER) python3 manage.py createsuperuser

down: ## Force stop and delete all containers.
	$(COMPOSE_COMMAND) down

shell: ## Run django shell.
	$(COMPOSE_COMMAND) $(RUN_LIKE_USER) python3 manage.py shell_plus

test: ##Run django unittest
	$(COMPOSE_COMMAND) $(RUN_LIKE_USER) python3 manage.py test

migrate: ## Run migrate command in django container.
		 ## use app=app_name to migrate just one application
	$(COMPOSE_COMMAND) $(RUN_LIKE_USER) python3 manage.py migrate $(app)

python_requirements: ## Install requirements on dev running container. To avoid rebuild the container.
	$(COMPOSE_COMMAND) exec web pip3 install -r /app/requirements.txt

makemigrations: ## Run makemigrations command in django container.
	$(COMPOSE_COMMAND) $(RUN_LIKE_USER) python3 manage.py makemigrations $(app)

logs: ## Show and follow all the logs
	$(COMPOSE_COMMAND) logs

resetdb: ## Clean database volume.
	docker volume rm web-pycones_db-data
