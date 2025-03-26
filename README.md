# API car-insurance-simulator

## Visão Geral

Esta API oferece uma interface para realizar a simulação de seguros para carros de maneira simples e eficiente.

## Índice

- [Recursos](#recursos)
- [Exemplo de Uso](#exemplo-de-uso)
- [Erros Comuns](#erros-comuns)
- [Ambiente de desenvolvimento](#ambiente-de-desenvolvimento)
- [Testes](#testes)
- [Diagramas](#diagramas)
- [Ajuda](#help)

## Recursos

A API oferece os seguintes recursos:

- **Insurance**: Operations related to insurance;

## Exemplo de Uso

### Utilizando cURL para realizar uma requisição GET para `/ping`

```bash
curl -X 'GET' \
  'http://localhost:5001/ping' \
  -H 'accept: application/json' \
```

## Erros Comuns

### 400 Bad Request

- **Descrição**: A requisição não pôde ser entendida devido a sintaxe inválida.

### 500 Internal Server Error

- **Descrição**: Erro interno no servidor. Isso pode ser causado por falhas no processamento da requisição ou problemas no servidor.
- **Code**: Código do Erro do sistema.

## Ambiente de desenvolvimento

Copie o arquivos "*.dist" e realize o preenchimento deles.

```shell
make copy-dist
```

Para rodar a tota a stack da API localmente, você precisa iniciar os containers do Banco de dados Mongo.

```shell
make infra-up
```

Para debugar a API local pare o container 'app' e sigua os passos abaixo.

```shell
make intall
make packages-dev
source venv/bin/acttivate
make run-api
```

Agora para acessar a API localmente utilize o link [API Docs](http://localhost:5000/docs)

## Testes

Para testar os endpoints da API, recomendamos o uso de ferramentas como o [Postman](https://www.postman.com/) ou [Insomnia](https://insomnia.rest/), onde você pode facilmente configurar requisições HTTP e testar os diferentes métodos da API.

Além disso, você pode rodar testes automatizados utilizando o comando:

```shell
make test
```

Para obter informações do coverage

```shell
make coverage
```

Para obter informações do Sonar Qube

```shell
make sonar-scan
```

## Diagramas

### Diagramas de classes

![Diagramas de classes](./docs/images/diagramas_de_classes/diagrama_de_classes_company.svg)

## Help?

```shell
make help
```
