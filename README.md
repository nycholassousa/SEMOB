# SEMOB - Consulta de Veículos no Pátio

A aplicação tem como foco uma consulta de veículos no Pátio da SEMOB.  O objetivo da aplicação é fazer com que pessoas que tenham seus carros rebocados (apreendidos) possam consultá-los para verificar sua situação pela web.

## Requisitos

- Python 3 (Não tenho certeza do 2)
- Pip
- PostgresSQL
- Linux

## Instalando

Implicando que você esteja no diretório principal da aplicação, apenas instale os requirimentos do pip
```sh
    pip install -r requirements
```

Após isso, execute os seguintes comandos:
```sh
    python
    from app import db
    db.create_all()
```

## Executando

Após ter instalado as requisições necessárias, entre no diretório principal e execute o seguinte comando:
```sh
    python app.py
```

A aplicação irá rodar localmente, na porta 5000 (http://127.0.0.1:5000)

## Informações Adicionais

TODO