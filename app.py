from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Client, Card
from logger import logger
from schemas import *
from flask_cors import CORS

from schemas.card import ListCardsSchema, show_cards

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
client_tag = Tag(name="Client", description="Adição, visualização e remoção de clientes à base")
card_tag = Tag(name="Card", description="Adição de um cartão à um cliente cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/client', tags=[client_tag],
          responses={"200": ClientViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_client(form: ClientSchema):
    """Adiciona um novo Cliente à base de dados

    Retorna uma representação dos clients e cartões associados.
    """
    client = Client(
        name=form.name,
        income=form.income,
        benefitClient=form.benefitClient)
    
    logger.info("adicionando Maria")
    logger.debug(f"Adicionando cliente de nome: '{client.name}'")
    try:
        # criando conexão com a base
        session = Session()
        logger.info("sessão criada")
        # adicionando client
        session.add(client)
        logger.info(f"sessão add {client.income} ")
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("sessão commit")
        logger.debug(f"Adicionado cliente de nome: '{client.name}'")
        return show_client(client), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{client.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo cadastro :/"
        logger.warning(f"Erro ao adicionar cliente '{client.name}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/clients', tags=[client_tag],
         responses={"200": ListClientsSchema, "404": ErrorSchema})
def get_clients():
    """Faz a busca por todos os Clientes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clients = session.query(Client).all()

    if not clients:
        # se não há clientes cadastrados
        return {"clients": []}, 200
    else:
        logger.debug(f"%d clientes encontrados" % len(clients))
        # retorna a representação de cliente
        print(clients)
        return show_clients(clients), 200


@app.get('/client', tags=[client_tag],
         responses={"200": ClientViewSchema, "404": ErrorSchema})
def get_client(query: ClientSearchSchema):
    """Faz a busca por um Cliente a partir do nome do cliente

    Retorna uma representação dos clientes e cartões associados.
    """
    client_name = query.name
    logger.debug(f"Coletando dados sobre cliente #{client_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    client = session.query(Client).filter(Client.name == client_name).first()

    if not client:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar client '{client_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Cliente econtrado: '{client.name}'")
        # retorna a representação de client
        return show_client(client), 200


@app.delete('/client', tags=[client_tag],
            responses={"200": ClientDelSchema, "404": ErrorSchema})
def del_client(query: ClientSearchSchema):
    """Deleta um Cliente a partir do nome de client informado

    Retorna uma mensagem de confirmação da remoção.
    """
    client_name = unquote(unquote(query.name))
    print(client_name)
    logger.debug(f"Deletando dados sobre client #{client_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Client).filter(Client.name == client_name).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado client #{client_name}")
        return {"message": "Client removido", "id": client_name}
    else:
        # se o client não foi encontrado
        error_msg = "Client não encontrado na base :/"
        logger.warning(f"Erro ao deletar client #'{client_name}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/card', tags=[card_tag],
          responses={"200": ClientViewSchema, "404": ErrorSchema})
def add_card(form: CardSchema):
    """Adiciona de um novo cartão à um clients cadastrado na base identificado pelo id

    Retorna uma representação dos clients e cartões associados.
    """
    client_id  = form.client_id
    logger.debug(f"Adicionando cartões ao client #{client_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo client
    client = session.query(Client).filter(Client.id == client_id).first()

    if not client:
        # se client não encontrado
        error_msg = "Client não encontrado na base :/"
        logger.warning(f"Erro ao adicionar cartão ao cliente '{client_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando o cartão

    name = form.name
    limit = form.limit
    benefitCard = form.benefitCard
    card = Card(name, limit, benefitCard)

    # adicionando o cartão ao client
    client.add_card(card)
    logger.info(f"nao Adicionado cartão ao cliente #{client_id}")
    session.commit()
    logger.info(f"sim Adicionado cartão ao cliente #{client_id}")

    # retorna a representação de client
    return show_client(client), 200

@app.get('/cards', tags=[card_tag],
         responses={"200": ListCardsSchema, "404": ErrorSchema})
def get_cards():
    """Faz a busca por todos os cartões cadastrados

    Retorna uma representação da listagem de cartões.
    """
    logger.debug(f"Coletando cartões ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cards = session.query(Card).all()

    if not cards:
        # se não há clientes cadastrados
        return {"cards": []}, 200
    else:
        logger.debug(f"%d clientes encontrados" % len(cards))
        # retorna a representação de cliente
        print(cards)
        return show_cards(cards), 200
    
