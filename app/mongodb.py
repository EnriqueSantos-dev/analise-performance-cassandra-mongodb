from pymongo import MongoClient
from generate_fake_data import get_random_region_and_state, format_cpf
import random
import uuid
from faker import Faker

faker = Faker()

mongo_url = 'mongodb://docker:root@localhost:27017'


class MongoDB:
    def __init__(self, table_names):
        self.table_names = table_names
        self.client = MongoClient(mongo_url)
        self.db = self.client['tbd']

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def generate_random_data_as_dict(self):
        region, state = get_random_region_and_state()
        name = faker.name()
        email = name.lower().replace(' ', '.') + '@gmail.com'

        return {
            "id": str(uuid.uuid4()),
            "name": name,
            "data_nascimento": faker.date_of_birth().strftime('%Y-%m-%d'),
            "cpf": format_cpf(str(faker.unique.random_number(digits=11))),
            "idade": random.randint(18, 80),
            "region": region,
            "state": state,
            "email": email,
        }

    def get_queries(self, collection_name):
        return {
            "select_all": lambda: self.get_collection(collection_name).find({}),
            "select_with_limite": lambda: self.get_collection(collection_name).find({}).limit(10000),
            "count": lambda: self.get_collection(collection_name).count_documents({}),
            "find_with_where_clausure": lambda: self.get_collection(collection_name).find({"regiao": "Nordeste", "estado": "AL"}),
            "find_with_where_clausure_without_partition_keys": lambda: self.get_collection(collection_name).find({"idade": {"$gte": 20, "$lte": 55}}),
            "insert_random_data": lambda: self.get_collection(collection_name).insert_one(self.generate_random_data_as_dict()),
            "insert_random_data_batch": lambda: self.get_collection(collection_name).insert_many([self.generate_random_data_as_dict() for _ in range(250)]),
            "update_many": lambda: self.get_collection(collection_name).update_many({"regiao": "Nordeste", "estado": "AL"}, {"$set": {"regiao": "Norte", "estado": "AM"}}),
        }
