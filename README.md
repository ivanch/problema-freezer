# Problema do Freezer

* Para rodar o programa:
```console
$ python main.py [argumentos]
```

### Argumentos disponíveis
| Nome | Descrição |
|----|---------|
|gerar|Gera novos dados de treino e teste|
|gerar-treino|Gera novos dados de treino apenas|
|gerar-teste|Gera novos dados de teste apenas |
|treinar|Treina e testa a árvore de decisão com os dados gerados |

* Se nenhum argumento for passado, será executado `gerar`, `treinar`.
* Valores padrões:
    * Treino
        * 50 refrigeradores
        * 25 refrigeradores defeituosos
    * Teste
        * 30 refrigeradores
        * 15 refrigeradores defeituosos
    * **Esses valores podem ser alterados em `main.py`**