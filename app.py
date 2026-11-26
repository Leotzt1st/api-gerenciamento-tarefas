import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


def criar_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(32)
    usuario = {'usuario': 'admin', 'senha': generate_password_hash('123456')}
    tarefas = [{'id': 1, 'titulo': 'Estudar API REST', 'situacao': 'pendente'}]

    def exigir_token(funcao):
        @wraps(funcao)
        def protegida(*args, **kwargs):
            partes = request.headers.get('Authorization', '').split()
            if len(partes) != 2 or partes[0].lower() != 'bearer':
                return jsonify(erro='Token obrigatório'), 401
            try:
                jwt.decode(partes[1], app.config['SECRET_KEY'], algorithms=['HS256'], options={'require': ['exp', 'sub']})
            except jwt.InvalidTokenError:
                return jsonify(erro='Token inválido ou expirado'), 401
            return funcao(*args, **kwargs)
        return protegida

    @app.post('/login')
    def login():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            dados = {}
        senha = dados.get('senha')
        if dados.get('usuario') != usuario['usuario'] or not isinstance(senha, str) or not check_password_hash(usuario['senha'], senha):
            return jsonify(erro='Credenciais incorretas'), 401
        token = jwt.encode({'sub': usuario['usuario'], 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify(token=token), 200

    @app.get('/tarefas')
    def consultar_tarefas():
        return jsonify(tarefas), 200

    @app.post('/tarefas')
    @exigir_token
    def cadastrar_tarefa():
        dados = request.get_json(silent=True)
        titulo = dados.get('titulo') if isinstance(dados, dict) else None
        if not isinstance(titulo, str) or not titulo.strip():
            return jsonify(erro='Título obrigatório'), 400
        tarefa = {'id': max((t['id'] for t in tarefas), default=0) + 1,
                  'titulo': titulo.strip(), 'situacao': 'pendente'}
        tarefas.append(tarefa)
        return jsonify(tarefa), 201

    return app


app = criar_app()

if __name__ == '__main__':
    app.run(port=5000)
