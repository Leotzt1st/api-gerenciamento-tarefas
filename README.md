# API de gerenciamento de tarefas

Nome: Leonardo Fernandes Tozato

## Executar no Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Endereço: http://127.0.0.1:5000

## Rotas (Bruno)

- POST /login: JSON `{"usuario":"admin","senha":"123456"}`. Retorna token e status 200, ou 401.
- GET /tarefas: retorna lista JSON e status 200, sem token.
- POST /tarefas: JSON `{"titulo":"Revisar os testes da API"}`. Envie o token recebido no cabeçalho Authorization: Bearer TOKEN. Retorna 201, 400 para título inválido ou 401 para token ausente/inválido.

A senha de demonstração é verificada por hash; o JWT expira em uma hora. Os dados ficam em memória e são reiniciados ao encerrar a API. A chave JWT é aleatória por execução, salvo configuração da variável SECRET_KEY. Credenciais de demonstração não devem ser usadas em produção.

## Testes

Em outro terminal, na pasta do projeto:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

São seis testes obrigatórios. Tire uma captura do resultado real e inclua no repositório antes de entregar. Não envie a pasta .venv.
