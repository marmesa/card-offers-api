from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from model import Session, Client, Card
from logger import logger
from schemas import *
from schemas.card import ListCardsSchema, show_cards

# Configuração da API
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags de documentação
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
client_tag = Tag(name="Client", description="Rotas para adição, visualização e remoção de clientes à base")
card_tag = Tag(name="Card", description="Rotas para adição e visualização de um cartão à um cliente cadastrado na base")

#@app.get('/', tags=[home_tag])
#def home():
#    """Redireciona para a tela de documentação."""
#    return redirect('/openapi')

@app.post('/client', tags=[client_tag],
          responses={"200": ClientViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_client(form: ClientSchema):
    """Adiciona um novo cliente à base de dados."""
    client = Client(
        name=form.name,
        income=form.income,
        benefitClient=form.benefitClient
    )

    logger.debug(f"Tentando adicionar cliente: {client.name}")
    try:
        session = Session()
        session.add(client)
        session.commit()
        logger.info(f"Cliente '{client.name}' adicionado com sucesso.")
        return show_client(client), 200

    except IntegrityError:
        error_msg = "Cliente de mesmo nome já salvo na base."
        logger.warning(f"Erro ao adicionar '{client.name}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo cadastro."
        logger.error(f"Erro inesperado ao adicionar '{client.name}': {e}")
        return {"message": error_msg}, 400

@app.get('/clients', tags=[client_tag],
         responses={"200": ListClientsSchema, "404": ErrorSchema})
def get_clients():
    """Retorna todos os clientes cadastrados."""
    logger.debug("Buscando todos os clientes...")
    session = Session()
    clients = session.query(Client).all()

    if not clients:
        return {"clients": []}, 200

    logger.info(f"{len(clients)} clientes encontrados.")
    return show_clients(clients), 200

@app.get('/client', tags=[client_tag],
         responses={"200": ClientViewSchema, "404": ErrorSchema})
def get_client(query: ClientSearchSchema):
    """Busca um cliente pelo nome."""
    client_name = query.name
    logger.debug(f"Buscando cliente: {client_name}")
    session = Session()
    client = session.query(Client).filter(Client.name == client_name).first()

    if not client:
        error_msg = "Cliente não encontrado na base."
        logger.warning(f"{client_name}: {error_msg}")
        return {"message": error_msg}, 404

    logger.info(f"Cliente encontrado: {client.name}")
    return show_client(client), 200

@app.delete('/client', tags=[client_tag],
            responses={"200": ClientDelSchema, "404": ErrorSchema})
def del_client(query: ClientSearchSchema):
    """Remove um cliente pelo nome."""
    client_name = unquote(unquote(query.name))
    logger.debug(f"Removendo cliente: {client_name}")
    session = Session()
    count = session.query(Client).filter(Client.name == client_name).delete()
    session.commit()

    if count:
        logger.info(f"Cliente removido: {client_name}")
        return {"message": "Client removido", "id": client_name}
    else:
        error_msg = "Cliente não encontrado na base."
        logger.warning(f"Erro ao remover '{client_name}': {error_msg}")
        return {"message": error_msg}, 404

@app.post('/card', tags=[card_tag],
          responses={"200": ClientViewSchema, "404": ErrorSchema})
def add_card(form: CardSchema):
    """Adiciona um novo cartão a um cliente existente."""
    client_id = form.client_id
    logger.debug(f"Adicionando cartão ao cliente ID: {client_id}")
    session = Session()
    client = session.query(Client).filter(Client.id == client_id).first()

    if not client:
        error_msg = "Cliente não encontrado na base."
        logger.warning(f"Erro ao adicionar cartão: {error_msg}")
        return {"message": error_msg}, 404

    card = Card(form.name, form.limit, form.benefitCard)
    client.add_card(card)
    session.commit()
    logger.info(f"Cartão '{form.name}' adicionado ao cliente ID {client_id}")
    return show_client(client), 200

@app.get('/cards', tags=[card_tag],
         responses={"200": ListCardsSchema, "404": ErrorSchema})
def get_cards():
    """Retorna todos os cartões cadastrados."""
    logger.debug("Buscando todos os cartões...")
    session = Session()
    cards = session.query(Card).all()

    if not cards:
        return {"cards": []}, 200

    logger.info(f"{len(cards)} cartões encontrados.")
    return show_cards(cards), 200