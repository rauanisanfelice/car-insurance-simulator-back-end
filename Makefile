.EXPORT_ALL_VARIABLES:
.PHONY: help clean coverage
.DEFAULT: help

-include .env
export $(shell sed 's/=.*//' .env)

PYTHONPATH := $(CURDIR)


help: ## Exibe a lista de comandos disponiveis
	@echo "Comandos disponiveis:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf " \033[36m%-20s\033[0m%s\n", $$1, $$2}' $(MAKEFILE_LIST)

format: ## Formata os arquivos python
	@echo "Formatando codigo..."
	@ruff format

lint:
	@echo "Verificando codigo..."
	@ruff check --fix


type-check:
	@echo "Verificando Mypy do codigo..."
	@mypy app --pretty


radon-cc:
	@echo "Verificando Complexidade Ciclomática do codigo..."
	@radon cc app


radon-mi:
	@echo "Verificando Manutenibilidade do codigo..."
	@radon mi app


radon-hal:
	@echo "Verificando Complexidade de Halstead do codigo..."
	@radon hal app


packages:
	@printf "Instalando bibliotecas..."
	@venv/bin/pip install -q --no-cache-dir -r requirements/base.txt
	@echo "OK"

packages-dev:
	@printf "Instalando bibliotecas de desenvolvimento..."
	@venv/bin/pip install -q --no-cache-dir -r requirements/dev.txt
	@echo "OK"

packages-test:
	@printf "Instalando bibliotecas de testes..."
	@venv/bin/pip install -q --no-cache-dir -r requirements/test.txt
	@echo "OK"


node-packages:
	@printf "Instalando node pacotes..."
	@npm install -s
	@echo "OK"

pip-upgrade:
	@printf "Atualizando pip..."
	@python -m pip install -q --upgrade pip
	@echo "Ok"

env-create: env-destroy
	@printf "Criando ambiente virtual... "
	@virtualenv -q venv -p python3.12
	@echo "OK"

env-destroy:
	@printf "Destruindo ambiente virtual... "
	@rm -rfd venv
	@echo "OK"

git-config-hooks:
	@printf "Configurando git hooks..."
	@git config --local core.hooksPath "$(PWD)/hooks"
	@chmod +x $(PWD)/hooks/*
	@echo "OK"


install: env-create pip-upgrade packages node-packages git-config-hooks
install-dev: env-create pip-upgrade packages-dev node-packages git-config-hooks

copy-dist:
	@printf "Copying dist files... "
	@cp .env.dist .env
	@cp docker-compose.yaml.dist docker-compose.yaml
	@echo "OK"

infra-up:
	@docker compose -p car-insurance-simulator-back-end up -d

infra-up-build:
	@docker compose -p car-insurance-simulator-back-end -f docker-compose.yaml up -d --build

infra-rebiuld:
	@docker compose -p car-insurance-simulator-back-end -f docker-compose.yaml up -d --build --force-recreate

infra-down:
	@docker compose -p car-insurance-simulator-back-end -f docker-compose.yaml down

docker-down:
	@docker compose down

docker-stop:
	@docker compose stop

run-api:
	@gunicorn --bind 0.0.0.0:5000 app.interface.api.main:app -w 1 -k uvicorn.workers.UvicornWorker --timeout 120

clear:
	@printf "Limpando arquivos temporários... "
	@rm -f dist/*.gz
	@rm -rfd *.egg-info
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@find . -type f -name '*.pyc' -delete
	@find . -type f -name '*.log' -delete
	@echo "OK"


test:
	@echo "Executando testes... "
	@py.test -vv -rxs --ignore=app/shared/exceptions.py

coverage: clear
	@LOG_LEVEL=50 py.test -xs --cov app --cov-report xml --cov-report term-missing

coverage-report: clear
	@LOG_LEVEL=50 py.test -xs --cov app --cov-report html --cov-report term-missing


sonar-up:
	@docker compose -f docker/sonarqube/docker-compose.yaml up -d

sonar-down:
	@docker compose -f docker/sonarqube/docker-compose.yaml down

sonar-scan: coverage sonar-up
	sed -i 's@$(PWD)@\/usr\/src@g' coverage.xml && \
	docker run \
		--rm \
		--network=host \
		-e SONAR_HOST_URL="http://127.0.0.1:9000" \
		-v "$(PWD):/usr/src" \
		sonarsource/sonar-scanner-cli \
		-Dsonar.host.url="http://127.0.0.1:9000" \
		-Dsonar.token=$(SONAR_TOKEN)


####################################
# Locale
####################################
locale-create-messages:
	@xgettext --from-code=utf-8 -d base --output app/locale/base.pot app/locale/messages.py
	@sed -i 's/charset=CHARSET/charset=UTF-8/g' app/locale/base.pot

locale-copy-template-to-langs:
	@cp app/locale/base.pot app/locale/pt_BR/LC_MESSAGES/base.po
	@cp app/locale/base.pot app/locale/en_US/LC_MESSAGES/base.po

locale-merge-messages: locale-create-messages
	@msgmerge --update app/locale/pt_BR/LC_MESSAGES/base.pot app/locale/base.pot
	@msgmerge --update app/locale/en_US/LC_MESSAGES/base.pot app/locale/base.pot

locale-compile-messages:
	@msgfmt -o app/locale/pt_BR/LC_MESSAGES/base.mo app/locale/pt_BR/LC_MESSAGES/base
	@msgfmt -o app/locale/en_US/LC_MESSAGES/base.mo app/locale/en_US/LC_MESSAGES/base

locale: locale-create-messages locale-copy-template-to-langs locale-merge-messages locale-compile-messages
