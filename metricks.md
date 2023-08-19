# Análise de performance dos SGBD Cassandra vs Mongodb

## Comparações

### Cassandra

- Muita dificuldade quando se trata de muitos dados.
- Não é uma boa opção para dados que precisam ser atualizados com frequência.
- Se um update incluir chave primária, acontece erros.
- A copia de dados é lenta e acontece erros com frequência.
- Não é possível atualizar um dados sem que todas as chaves primárias sejam incluídas.

### MongoDB

- Lidou de forma bem melhor com os dados.
- Não teve problemas com updates.
- A copia de dados foi bem mais rápida e sem erros.

## Cassandra

Resultado das cópias de dados para o Cassandra

| rows | time    |
| ---- | ------- |
| 100K | 5.422s  |
| 1M   | 32.872s |
| 10M  | 240s    |

## MongoDB

Resultado das cópias de dados para o MongoDB

| rows | time    |
| ---- | ------- |
| 100K | 2.146s  |
| 1M   | 24.858s |
| 10M  | 229s    |

### Resultados das queries Cassandra

| Tabela       | Query                               | Tempo de execução        |
| ------------ | ----------------------------------- | ------------------------ |
| PERSONS_100K | SELECT_ALL                          | 0.042973s                |
| PERSONS_100K | SELECT_WITH_LIMITE                  | 0.043892s                |
| PERSONS_100K | COUNT                               | 0.610391s                |
| PERSONS_100K | SELECT_WHERE_WITH_PARTITION_KEYS    | 0.148200s                |
| PERSONS_100K | SELECT_WHERE_WITHOUT_PARTITION_KEYS | 0.095472s                |
| PERSONS_100K | INSERT_RANDOM_DATA                  | 0.002432s                |
| PERSONS_100K | INSERT_WITH_BATCH_OP_RANDOM_DATA    | 0.084221s                |
| PERSONS_100K | UPDATE_MANY                         | Erro ao executar a query |
| PERSONS_1M   | SELECT_ALL                          | 0.094166s                |
| PERSONS_1M   | SELECT_WITH_LIMITE                  | 0.055887s                |
| PERSONS_1M   | COUNT                               | 7.123725s                |
| PERSONS_1M   | SELECT_WHERE_WITH_PARTITION_KEYS    | 0.416848s                |
| PERSONS_1M   | SELECT_WHERE_WITHOUT_PARTITION_KEYS | 0.150458s                |
| PERSONS_1M   | INSERT_RANDOM_DATA                  | 0.001944s                |
| PERSONS_1M   | INSERT_WITH_BATCH_OP_RANDOM_DATA    | 0.050036s                |
| PERSONS_1M   | UPDATE_MANY                         | Erro ao executar a query |
| PERSONS_10M  | SELECT_ALL                          | 0.056623s                |
| PERSONS_10M  | SELECT_WITH_LIMITE                  | 0.063676s                |
| PERSONS_10M  | COUNT                               | Erro ao executar a query |
| PERSONS_10M  | SELECT_WHERE_WITH_PARTITION_KEYS    | 0.459787s                |
| PERSONS_10M  | SELECT_WHERE_WITHOUT_PARTITION_KEYS | 0.072284s                |
| PERSONS_10M  | INSERT_RANDOM_DATA                  | 0.002012s                |
| PERSONS_10M  | INSERT_WITH_BATCH_OP_RANDOM_DATA    | 0.075296s                |
| PERSONS_10M  | UPDATE_MANY                         | Erro ao executar a query |

### Resultados das queries MongoDB

| Tabela       | Query                                           | Tempo de execução |
| ------------ | ----------------------------------------------- | ----------------- |
| PERSONS_100K | SELECT_ALL                                      | 0.000082s         |
| PERSONS_100K | SELECT_WITH_LIMITE                              | 0.000018s         |
| PERSONS_100K | COUNT                                           | 0.040851s         |
| PERSONS_100K | FIND_WITH_WHERE_CLAUSURE                        | 0.000092s         |
| PERSONS_100K | FIND_WITH_WHERE_CLAUSURE_WITHOUT_PARTITION_KEYS | 0.000028s         |
| PERSONS_100K | INSERT_RANDOM_DATA                              | 0.001433s         |
| PERSONS_100K | INSERT_RANDOM_DATA_BATCH                        | 0.044429s         |
| PERSONS_100K | UPDATE_MANY                                     | 0.052619s         |
| PERSONS_1M   | SELECT_ALL                                      | 0.000072s         |
| PERSONS_1M   | SELECT_WITH_LIMITE                              | 0.000029s         |
| PERSONS_1M   | COUNT                                           | 0.001394s         |
| PERSONS_1M   | FIND_WITH_WHERE_CLAUSURE                        | 0.000038s         |
| PERSONS_1M   | FIND_WITH_WHERE_CLAUSURE_WITHOUT_PARTITION_KEYS | 0.000018s         |
| PERSONS_1M   | INSERT_RANDOM_DATA                              | 0.000986s         |
| PERSONS_1M   | INSERT_RANDOM_DATA_BATCH                        | 0.031710s         |
| PERSONS_1M   | UPDATE_MANY                                     | 0.001758s         |
| PERSONS_10M  | SELECT_ALL                                      | 0.000057s         |
| PERSONS_10M  | SELECT_WITH_LIMITE                              | 0.000027s         |
| PERSONS_10M  | COUNT                                           | 0.001280s         |
| PERSONS_10M  | FIND_WITH_WHERE_CLAUSURE                        | 0.000034s         |
| PERSONS_10M  | FIND_WITH_WHERE_CLAUSURE_WITHOUT_PARTITION_KEYS | 0.000011s         |
| PERSONS_10M  | INSERT_RANDOM_DATA                              | 0.000975s         |
| PERSONS_10M  | INSERT_RANDOM_DATA_BATCH                        | 0.031754s         |
| PERSONS_10M  | UPDATE_MANY                                     | 0.001601s         |
