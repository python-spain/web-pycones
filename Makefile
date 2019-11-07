.PHONY: help

.DEFAULT_GOAL := help


help: ## This help.
	@echo
	@echo "\e[1;35m Port mapping used: $<\e[0m"
	@echo "\e[1;33m - Backend: localhost:8000 $<\e[0m"
	@echo
	@echo "\e[1;36m Testing database credentials in file .envs/.local/.postgres $<\e[0m"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo


build: 
	docker-compose -f dev.yml build

up: 
	docker-compose -f dev.yml up

silenceup: ## Run developer containers without print messages.
	docker-compose -f dev.yml up -d

createsuperuser: ## Create superuser.
	docker-compose -f dev.yml run --rm backend python3 manage.py createsuperuser

down: ## Force stop and delete all containers.
	docker-compose  -f dev.yml down

shell: ## Run django shell.
	docker-compose -f dev.yml run  --rm backend python3 manage.py shell_plus

test: ##Run django unittest
	docker-compose -f dev.yml run --rm backend python3 manage.py test

migrate: ## Run migrate command in django container.
	docker-compose -f dev.yml run  --rm backend python3 manage.py migrate

makemigrations: ## Run makemigrations command in django container.
	docker-compose -f dev.yml run   --rm backend python3 manage.py makemigrations

logs: ## Show and follow the django console messages
	docker-compose -f dev.yml logs backend

resetdb: ## Clean database volume.
	docker volume rm web-pycones_db-data

gulp: ## Gulp, compile sass and js.
	docker-compose -f dev.yml run --rm  backend gulp

gulpbuild: ## Gulp build, compile sass and js.
	docker-compose -f dev.yml run --rm  backend gulp build
