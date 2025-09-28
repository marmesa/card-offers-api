# 💳 card-offers-api

Este projeto é parte da entrega do curso de Desenvolvimento Full Stack Básico da pós-graduação da PUC-Rio.  
Trata-se do back-end de uma aplicação voltada para o cadastro de clientes e cartões, com o objetivo futuro de recomendar o melhor cartão com base nas características do cliente.

---

## 🚀 Como executar o projeto

### 1. Pré-requisitos

- Python 3 instalado  
- Ambiente virtual configurado (recomendado)  
- Todas as bibliotecas listadas no `requirements.txt`

### 2. Clonando o repositório

```bash
git clone <URL-do-repositório>
cd card-offers-api
```

### 3. Criando e ativando o ambiente virtual

Criação

python -m venv meu-env 
ou 
python3 -m venv meu-env 

Ativação 

.\meu-env\Scripts\activate

💡É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### 4. Instalando as dependências

pip install -r requirements.txt

### 5. Executando a API

flask run --host 0.0.0.0 --port 5000

#### Modo de desenvolvimento (com reload automático)

flask run --host 0.0.0.0 --port 5000 --reload

## 🧩 Interface de documentação
Caso a interface Swagger ou Redoc não esteja disponível, instale os componentes adicionais:

pip install -U flask-openapi3[swagger,redoc,rapidoc,rapipdf,scalar,elements]

## Aplicação

Abra o [http://localhost:5000/openapi/](http://localhost:5000/openapi/) no navegador para verificar o status da API em execução.