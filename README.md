# MyFileExplorer

[![CircleCI](https://circleci.com/gh/JvitorS23/myFileExplorer.svg?style=svg)](https://circleci.com/gh/JvitorS23/myFileExplorer)

Sistema de arquivos feito com Python e Django.

## Tecnologias utilizadas:

* Python
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)

## Execução da aplicação

### Variáveis de ambiente

A maior parte das configurações do projeto é através de variáveis de ambiente. É preciso criar um arquivo `.env` na 
raiz do repositório seguindo o modelo do arquivo `.env-example`.

### Iniciar aplicação usando [Docker](https://www.docker.com/) (recomendado):
```bash
 docker-compose up --build
```
O docker fará o build de uma imagem personalizada, já instalando as dependências necessárias (requirements.txt), em seguida, o servidor de desenvolvimento estará acessível em: [http://localhost:8000](http://localhost:8000). Além do container rodando o servidor Django, o docker-compose também cria um container para o PostgreSQL (banco de dados usado pela aplicação).

### Iniciar a aplicação sem usar Docker:

- Instalação das dependências (é recomendado usar um virtualenv):
```bash
 pip install -r requirements.txt
```
Em seguida, é preciso [baixar e instalar o PostgreSQL](https://www.postgresql.org/download/), criar uma base de dados para a aplicação e configurar as credenciais do banco como variáveis de ambiente no arquivo .env.

- Rodar migrations e iniciar servidor de desenvolvimento:
```bash
 python manage.py migrate 
 python manage.py runserver 0.0.0.0:8000
```
O servidor de desenvolvimento estará acessível em: [http://localhost:8000](http://localhost:8000).
