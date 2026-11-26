import pytest
from app import criar_app


@pytest.fixture
def cliente():
    app = criar_app()
    app.config['TESTING'] = True
    return app.test_client()


def obter_token(cliente):
    resposta = cliente.post('/login', json={'usuario': 'admin', 'senha': '123456'})
    return resposta.get_json()['token']


def test_login_correto(cliente):
    resposta = cliente.post('/login', json={'usuario': 'admin', 'senha': '123456'})
    assert resposta.status_code == 200
    assert resposta.get_json()['token']


def test_login_senha_incorreta(cliente):
    resposta = cliente.post('/login', json={'usuario': 'admin', 'senha': 'errada'})
    assert resposta.status_code == 401
    assert 'token' not in resposta.get_json()


def test_consulta_tarefas(cliente):
    resposta = cliente.get('/tarefas')
    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


def test_cadastro_sem_token(cliente):
    antes = cliente.get('/tarefas').get_json()
    resposta = cliente.post('/tarefas', json={'titulo': 'Nova tarefa'})
    assert resposta.status_code == 401
    assert cliente.get('/tarefas').get_json() == antes


def test_cadastro_token_valido(cliente):
    antes = cliente.get('/tarefas').get_json()
    resposta = cliente.post('/tarefas', json={'titulo': 'Nova tarefa'}, headers={'Authorization': 'Bearer ' + obter_token(cliente)})
    assert resposta.status_code == 201
    tarefa = resposta.get_json()
    assert tarefa['titulo'] == 'Nova tarefa'
    assert tarefa['situacao'] == 'pendente'
    assert tarefa['id'] not in [t['id'] for t in antes]
    assert cliente.get('/tarefas').get_json() == antes + [tarefa]


def test_cadastro_titulo_vazio(cliente):
    antes = cliente.get('/tarefas').get_json()
    headers = {'Authorization': 'Bearer ' + obter_token(cliente)}
    for dados in ({'titulo': ''}, {'titulo': '   '}, {}):
        resposta = cliente.post('/tarefas', json=dados, headers=headers)
        assert resposta.status_code == 400
        assert cliente.get('/tarefas').get_json() == antes
