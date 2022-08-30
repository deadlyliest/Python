USE ZZironiteDB;

CREATE TABLE carros (
    id integer not null auto_increment,
    marca varchar(100),
    modelo varchar(100),
    ano integer,
    id_carro varchar(50),
    PRIMARY KEY (id)
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

INSERT INTO carros (marca, modelo, ano) VALUES ('Fiat', 'Marea', 1999,'1342a330-9a14-4560-807b-1d9e682c715f');
INSERT INTO carros (marca, modelo, ano) VALUES ('Fiat', 'Uno', 1992, '685b0e43-4ddc-41f5-bc29-dca0aa960ca5');
INSERT INTO carros (marca, modelo, ano) VALUES ('Ford', 'Escort', 1985, '2d1173d6-d56a-43de-b371-87c57c232b4f');
INSERT INTO carros (marca, modelo, ano) VALUES ('Chevrolet', 'Chevette', 1978. '4c39bddc-fe8c-455e-b4f8-6cae05295ba3');
INSERT INTO carros (marca, modelo, ano) VALUES ('Volkswagem', 'Fusca', 1962, 'a0ce1a1b-69f1-4bb4-8438-efdfce172d37');