# Problema do Freezer

## Rodar localmente

1. Em primeiro lugar, é necessário possuir o `Python 3.x` e o gerenciador de pacotes `pip` instalado.
2. Em seguida, para instalar as dependências:
```console
$ pip install -r requirements.txt
```

2. Para rodar o programa, basta utilizar:
```console
$ python main.py [argumentos]
```

### Argumentos disponíveis
| Nome | Descrição |
|----|---------|
|gen          |Gera novos dados de treino e teste                      |
|gen-train    |Gera novos dados de treino apenas                       |
|gen-test     |Gera novos dados de teste apenas                        |
|train        |Treina e testa a árvore de decisão com os dados gerados |
|predict `maquina.csv`|Verifica se o arquivo `maquina.csv` é defeituoso ou confiável, com base em um treino pré estabelecido                                 |
|mock-faulty `maquina.csv`|Cria um arquivo `maquina.csv` defeituoso                |
|mock-reliable `maquina.csv`|Cria um arquivo `maquina.csv` confiável                 |

* Se nenhum argumento for passado, será executado `gerar` e `treinar`.
* Valores padrões:
    * Tamanho do conjunto de dados de treino
        * 50 refrigeradores
        * 25 refrigeradores defeituosos
    * Tamanho do conjunto de dados de teste
        * 30 refrigeradores
        * 15 refrigeradores defeituosos
    * **Esses valores podem ser alterados em `main.py`**
* O arquivo de modelo treinado do algoritmo será salvo em `data/decision-tree.pkl`
* O arquivo de visualização do modelo treinado será salvo em `data/viz.pdf`
