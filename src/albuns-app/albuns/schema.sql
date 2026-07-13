DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS usuario;


CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);


CREATE TABLE album (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    artista TEXT NOT NULL,
    genero TEXT,
    ano INTEGER,
    descricao TEXT,
    criado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);