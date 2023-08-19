import pandas as pd
import uuid
import random
from faker import Faker
import time

faker = Faker()


def get_random_region_and_state():
    states_of_regions = {
        "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
        "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
        "Centro-Oeste": ["DF", "GO", "MS", "MT"],
        "Sudeste": ["ES", "MG", "RJ", "SP"],
        "Sul": ["PR", "RS", "SC"]
    }

    random_region = random.choice(list(states_of_regions.keys()))
    random_state = random.choice(states_of_regions[random_region])

    return random_region, random_state


def format_cpf(numero):
    cpf_formatado = f'{numero[:3]}.{numero[3:6]}.{numero[6:9]}-{numero[9:]}'
    return cpf_formatado


def generate_fake_data_in_chunks(range_number, arquivo_name, chunk_size=10000):
    print(f'Gerando {range_number} registros em chunks...')
    time_start = time.time()

    num_chunks = range_number // chunk_size

    for chunk_idx in range(num_chunks):
        data_list = []

        for _ in range(chunk_size):
            region, state = get_random_region_and_state()
            name = faker.name()
            email = name.lower().replace(' ', '.') + '@gmail.com'

            data_list.append({
                'id': str(uuid.uuid4()),
                'name': name,
                'data_nascimento': faker.date_of_birth().strftime('%Y-%m-%d'),
                'cpf': format_cpf(str(faker.unique.random_number(digits=11))),
                'idade': random.randint(18, 80),
                'regiao': region,
                'estado': state,
                'email': email,
            })

        df = pd.DataFrame(data_list)
        if chunk_idx == 0:
            df.to_csv(arquivo_name, mode='w', index=False)
        else:
            df.to_csv(arquivo_name, mode='a', header=False, index=False)

    time_end = time.time()
    print(
        f'Tempo total de execução para {range_number}: {time_end - time_start} segundos')


if __name__ == '__main__':
    generate_fake_data_in_chunks(
        50000000, '50M_persons.csv', chunk_size=100000)
