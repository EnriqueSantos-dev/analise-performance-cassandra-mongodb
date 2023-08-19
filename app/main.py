from cassandra_db import Cassandra
from mongodb import MongoDB
import time

table_names = ["persons_100K",
               "persons_1M", "persons_10M"]


class QueriesResources:
    def __init__(self, table_names):
        self.table_names = table_names

    def get_query_time(self, query):
        try:
            start_time = time.time()
            query()
            end_time = time.time()
            execution_time = end_time - start_time
            return f"{execution_time:.6f}s"
        except Exception as e:
            return "Erro ao executar a query"

    def run_queries(self, db_name, get_queries_fn):
        markdown_output = ""
        markdown_output = f"\n### Resultados das queries {db_name}\n\n"
        markdown_output += f"| Tabela | Query | Tempo de execução |\n"
        markdown_output += f"| ------ | ----- | ----------------- |\n"

        for table_name in self.table_names:
            for query_key, query in get_queries_fn(table_name).items():
                markdown_output += f"| {table_name.upper()} | {query_key.upper()} | {self.get_query_time(query)} |\n"

        print(markdown_output)


if __name__ == "__main__":
    cassandra = Cassandra(table_names)
    cassandra_queries = cassandra.get_queries

    mongodb = MongoDB(table_names)
    mongodb_queries = mongodb.get_queries

    queries_resources = QueriesResources(table_names)

    queries_resources.run_queries("Cassandra", cassandra_queries)
    queries_resources.run_queries("MongoDB", mongodb_queries)
