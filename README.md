# Análise de performance do SGBD Cassandra e do MongoDB

## Requisitos

- Para executar esse projeto vc precisa ter instalado em sua máquina o docker e o plugin do docker-compose.
- Conhecimento básico em docker.
- Conhecimento básico em python.

## Como executar

### Clonando o projeto

Clone o projeto na sua máquina e entre na pasta do projeto. Via o comando abaixo para quem usa sistema unix ou abrindo diretamente a pasta na sua IDEA preferida.

```sh
git clone https://github.com/enriquesantos-dev/analise-performance-cassandra-mongodb.git
```

```sh
cd analise-performance-cassandra-mongodb
```

### Datasets

Para executar esse projeto vc precisa ter datasets em formato csv com tamanhos de 100K, 1M e 10M, para isso vou deixar o link para uma pasta do google drive, baixe o arquivo e siga o passo a passo. Contudo, se vc quiser pode criar seus próprios datasets, rodando localmente o script `generate_fake_data.py` que está na pasta `app` desse projeto e passar os valores do datasets.

Link para os datasets: [datasets](https://drive.google.com/drive/u/2/folders/1BOS-zWaUa-NzVcp6irjzmgmHrFVVvpEY)

o formato que os dados devem ter é o seguinte:

```py
{
    'id': str, # uuid
    'name': str,
    'data_nascimento': str, # formato: yyyy/mm/dd
    'cpf': str,
    'idade': int,
    'regiao': str,
    'estado': str,
    'email': str,
}
```

Depois de baixar os datasets faça o unzip, crie a pasta `./docker/data` e mova os csv para essa pasta.

### Docker

Vamos "subir" os containers do cassandra e do mongo, para isso execute o comando abaixo:

```sh
docker compose up -d
```

#### Criando as tabelas, KEYSPACE e copiando os datasets para o container do cassandra

Entrando no container do cassandra:

```sh
docker exec -it cassandra-tbd1 bash
```

Dentro do container do cassandra execute o seguinte comando:

```sh
cqlsh
```

Criando o KEYSPACE:

```sh
CREATE KEYSPACE tbd WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'replication_factor' : 2 };
USE tbd;
```

Criando as tabelas:

```cql
CREATE TABLE persons_100K (
   id UUID,
   name VARCHAR,
   data_nascimento DATE,
   cpf VARCHAR,
   idade INT,
   regiao VARCHAR,
   estado VARCHAR,
   email VARCHAR,
   PRIMARY KEY ((id), regiao, estado, data_nascimento)
);

CREATE TABLE persons_1M (
   id UUID,
   name VARCHAR,
   data_nascimento DATE,
   cpf VARCHAR,
   idade INT,
   regiao VARCHAR,
   estado VARCHAR,
   email VARCHAR,
   PRIMARY KEY ((id), regiao, estado, data_nascimento)
);

CREATE TABLE persons_10M (
   id UUID,
   name VARCHAR,
   data_nascimento DATE,
   cpf VARCHAR,
   idade INT,
   regiao VARCHAR,
   estado VARCHAR,
   email VARCHAR,
   PRIMARY KEY ((id), regiao, estado, data_nascimento)
);
```

Copiando os datasets para o cassandra:
Esse é um processo demorado, então tenha paciência. Também pode ocorrer erros de timeout, se isso acontecer, se acontece apenas aguarda a conclusão.

Obs: se acontecer error pode ser que nem todas as linhas sejam copiadas, então vc pode executar o comando novamente.

```sh
COPY persons_100K (id, name, data_nascimento, cpf, idade, regiao, estado, email) FROM '/home/datasets/100K_persons.csv' WITH HEADER=true;

COPY persons_1M (id, name, data_nascimento, cpf, idade, regiao, estado, email) FROM '/home/datasets/1M_persons.csv' WITH HEADER=true;

COPY persons_10M (id, name, data_nascimento, cpf, idade, regiao, estado, email) FROM '/home/datasets/10M_persons.csv' WITH HEADER=true;
```

#### Criando o banco de dados e copiando os datasets para o mongo

Entrando no container do mongo:

```sh
docker exec -it mongodb mongosh -u docker -p root
```

Criando o banco com o nome `tbd`:

```sh
use tbd
```

Criando as coleções:

```sh
db.createCollection('persons_100K');
db.createCollection('persons_1M');
db.createCollection('persons_10M');
exit
```

Copiando os datasets para o mongo:

```sh
docker exec -it mongodb bash
```

```sh
mongoimport -u docker -p root --authenticationDatabase=admin --db tbd --collection=persons_100K --type=csv --file=/home/datasets/100K_persons.csv --fields="id","name","data_nascimento","cpf","idade","regiao","estado","email";

mongoimport -u docker -p root --authenticationDatabase=admin --collection=persons_1M --type=csv --file=/home/datasets/1M_persons.csv --fields="id","name","data_nascimento","cpf","idade","regiao","estado","email";

mongoimport -u docker -p root --authenticationDatabase=admin --collection=persons_10M --type=csv --file=/home/datasets/10M_persons.csv --fields="id","name","data_nascimento","cpf","idade","regiao","estado","email";
```

## Executando o projeto

Criando o ambiente virtual para o python:

```sh
python3 -m venv venv
source venv/bin/activate
```

Instalando as dependências:

```sh
pip3 install -r ./app/requirements.txt
```

Executando o projeto com o comando:

```bash
python3 app/main.py
```

Obs: É possível colocar os resultados em um arquivo .md usando o comando abaixo:

```sh
python3 app/main.py > results.md
```
