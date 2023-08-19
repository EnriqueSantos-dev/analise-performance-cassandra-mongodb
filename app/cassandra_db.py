from cassandra.cluster import Cluster
from generate_fake_data import format_cpf, get_random_region_and_state
import random
import uuid
from faker import Faker

faker = Faker()


class Cassandra:
    def __init__(self, table_names):
        self.table_names = table_names
        self.cluster = Cluster(['172.18.0.2'])
        self.session = self.cluster.connect('tbd')

    def insert_random_data(self, table_name):
        name = faker.name()
        email = name.lower().replace(' ', '.') + '@gmail.com'

        region, state = get_random_region_and_state()

        return f"""INSERT INTO tbd.{table_name} (id, name, data_nascimento, cpf, idade, regiao, estado, email) VALUES ({str(uuid.uuid4())}, '{name}', '{faker.date_of_birth().strftime('%Y-%m-%d')}', '{format_cpf(str(faker.unique.random_number(digits=11)))}', {random.randint(18, 80)}, '{region}', '{state}', '{email}');"""

    def batch_query(self, table_name, batch_size=250):
        query = f"""BEGIN BATCH\n"""
        for _ in range(batch_size):
            query += self.insert_random_data(table_name) + '\n'
        query += f"""APPLY BATCH;"""

        return query

    def get_queries(self, table_name):
        return {
            "select_all": lambda: self.session.execute(f"SELECT * FROM tbd.{table_name}"),
            "select_with_limite": lambda: self.session.execute(f"SELECT * FROM tbd.{table_name} LIMIT 10000"),
            "count": lambda: self.session.execute(f"SELECT COUNT(*) FROM tbd.{table_name} ALLOW FILTERING;"),
            "select_where_with_partition_keys": lambda: self.session.execute(f"""SELECT * FROM tbd.{table_name} WHERE regiao = 'Nordeste' AND estado = 'AL' ALLOW FILTERING;"""),
            "select_where_without_partition_keys": lambda: self.session.execute(f"""SELECT * FROM tbd.{table_name} WHERE idade >= 20 AND idade <= 55 ALLOW FILTERING;"""),
            "insert_random_data": lambda: self.session.execute(self.insert_random_data(table_name)),
            "insert_with_batch_op_random_data": lambda: self.session.execute(self.batch_query(table_name)),
            "update_many": lambda: self.session.execute(f"""UPDATE tbd.{table_name} SET regiao = 'Norte', estado = 'AM' WHERE regiao = 'Nordeste' AND estado = 'AL';""")}
