# MyFileExplorer

[![CircleCI](https://circleci.com/gh/JvitorS23/myFileExplorer.svg?style=svg)](https://circleci.com/gh/JvitorS23/myFileExplorer)

Sistema de arquivos feito com Python e Django. Aplicação que permite um usuário criar pastas e arquivos, os arquivos são armazenados no S3.

## Tecnologias utilizadas:

* Python
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Docker](https://www.docker.com/)
* [CircleCI](https://circleci.com/)
* [Caddy](https://caddyserver.com/)
* [gunicorn](https://gunicorn.org/)
* [AWS S3](https://aws.amazon.com/pt/s3/)
* [AWS EC2](https://aws.amazon.com/pt/ec2/)


## Detalhes da aplicação

O projeto Django possui 2 apps, eles são:

* User: Responsável pela criação e autenticação de usuários (Autenticação JWT) 
   * Rota de login: ```/api/user/login```
   * Rotas para tokens: ```/api/token```
   * Rota de registro de um novo usuário: ```/api/user/register```
   * Rota de logout: ```/api/user/logout```
* Explorer: Responsável pelo CRUD de pastas e arquivos. Esse app possui dois models: Folder e File. Eles são as 
  entidades principais da aplicação, cada arquivo ou pasta se relaciona com seu usuário dono. Além disso, todo novo 
  usuário possui uma pasta raiz, criada automaticamente e que não pode ser editada. Uma pasta ou arquivo possui uma 
  pasta pai (exceto a pasta raiz do usuário). 
  
  <p align="center">
    <img src="https://user-images.githubusercontent.com/52494917/163726459-48eae00e-1679-4b9f-aef9-8ba2fbae7b5e.png" />
  </p>
  
   * CRUD de pastas ```/api/folder```
   * CRUD de arquivos ```/api/file```
   * Listagem de objetos de uma pasta ```/api/list-folder/<id>```

### Features:
* Login e registro de usuários
* Autenticação para acessar API
* CRUD de pastas e arquivos 
* Arquivos armazenados no S3
* Testes automatizados para todas as rotas da API
* CircleCI para pipelines de qualidade de código (lint, build e execução de testes)


## Documentação das API's (swagger)

A documentação da API está disponível em:

https://3.234.194.198.nip.io/api/swagger


## Deploy
O deploy da aplicação foi feito usando a AWS (EC2), Docker e o Caddy. Na pasta ```deploy``` existe um arquivo docker-compose.yml que possui 3 serviços:
* Postgres: Banco de dados SQL usado pela aplicação (também é possível utilizar bancos hospedados em serviços como o RDS, basta apenas alterar as credencias do banco no arquivo .env).
* django: Serviço que roda a aplicação Python. Possui um Dockerfile personalizado (```deploy/django/Dockerfile```)  e utiliza o gunicorn como servidor wsgi.
* Caddy: É um servidor HTTP que serve os arquivos estáticos e faz o proxy para o gunicorn servir rotas não estáticas. Instala certificado HTTPS automaticamente usando o Let's encrypt.

A aplicação pode ser acessada em: 

https://3.234.194.198.nip.io/api/swagger

## Execução da aplicação

### Variáveis de ambiente

A maior parte das configurações do projeto é através de variáveis de ambiente. É preciso criar um arquivo `.env` na 
raiz do repositório seguindo o modelo do arquivo `.env-example`.

### Iniciar aplicação usando [Docker](https://www.docker.com/) (recomendado):
```bash
 docker-compose up --build
```
O docker fará o build de uma imagem personalizada, já instalando as dependências necessárias (requirements.txt), em seguida, o servidor de desenvolvimento estará acessível em: [http://localhost:8000](http://localhost:8000). Além do container rodando o servidor Django, o docker-compose também cria um container para o PostgreSQL (banco de dados usado pela aplicação).

