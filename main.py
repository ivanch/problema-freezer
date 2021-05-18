import sys

from cart import CART

# CONSTS

# Train
AMOUNT_OF_FREEZERS = 50
AMOUNT_OF_FAULTY_FREEZERS = 25

# Test
TEST_AMOUNT_OF_FREEZERS = 30
TEST_AMOUNT_OF_FAULTY_FREEZERS = 15

args = sys.argv[1:]

cart = CART()

def generate_train_data():
    print("Gerando dados de treino...")
    cart.generate_train_data(AMOUNT_OF_FREEZERS, AMOUNT_OF_FAULTY_FREEZERS)

def generate_test_data():
    print("Gerando dados de teste...")
    cart.generate_test_data(TEST_AMOUNT_OF_FREEZERS, TEST_AMOUNT_OF_FAULTY_FREEZERS)

def train():
    print("Treinando árvore de decisão...")
    cart.train(AMOUNT_OF_FREEZERS)
    print("Gerando visualização da árvore de decisão...")
    cart.generate_visualization()

def test():
    print("Testando árvore de decisão...")
    cart.test(TEST_AMOUNT_OF_FREEZERS)

if (len(args) == 0):
    generate_train_data()
    generate_test_data()
    train()
    test()

if "gerar" in args:
    generate_train_data()
    generate_test_data()

if "gerar-treino" in args:
    generate_train_data()
if "gerar-teste" in args:
    generate_test_data()

if "treinar" in args:
    train()
    test()