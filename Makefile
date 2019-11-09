.PHONY: help

.DEFAULT_GOAL := help


help: ## This help.
	@echo
	@echo "\e[1;35m Port mapping used: $<\e[0m"
	@echo "\e[1;33m - Backend: localhost:8000 $<\e[0m"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo


build:
	docker-compose -f dev.yml build

up:
	docker-compose -f dev.yml up

upd: ## Run developer containers without print messages.
	docker-compose -f dev.yml up -d

createsuperuser: ## Create superuser.
	docker-compose -f dev.yml run --rm web python3 manage.py createsuperuser

down: ## Force stop and delete all containers.
	docker-compose  -f dev.yml down

shell: ## Run django shell.
	docker-compose -f dev.yml run  --rm web python3 manage.py shell_plus

test: ##Run django unittest
	docker-compose -f dev.yml run --rm web python3 manage.py test

migrate: ## Run migrate command in django container.
	docker-compose -f dev.yml run  --rm web python3 manage.py migrate $(app)

python_requirements: ## Install requirements on dev running container. To avoid rebuild the container.
	docker-compose -f dev.yml exec web pip3 install -r /requirements/production.txt
	docker-compose -f dev.yml exec web pip3 install -r /requirements/local.txt

makemigrations: ## Run makemigrations command in django container.
	docker-compose -f dev.yml run   --rm web python3 manage.py makemigrations $(app)

logs: ## Show and follow all the logs
	docker-compose -f dev.yml logs

resetdb: ## Clean database volume.
	docker volume rm web-pycones_db-data
