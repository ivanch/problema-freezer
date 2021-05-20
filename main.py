import sys
import os

from utils.utils import program_error
from cart import CART
from generator import Generator

# CONSTS

# Train
AMOUNT_OF_FREEZERS = 50
AMOUNT_OF_FAULTY_FREEZERS = 25

# Test
TEST_AMOUNT_OF_FREEZERS = 30
TEST_AMOUNT_OF_FAULTY_FREEZERS = 15

args = sys.argv[1:]

cart = CART()

if not os.path.exists("data"):
    os.makedirs("data")

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
    cart.save_tree()

def test():
    print("Testando árvore de decisão...")
    cart.test(TEST_AMOUNT_OF_FREEZERS)

if (len(args) == 0):
    generate_train_data()
    generate_test_data()
    train()
    test()

if "gen" in args:
    generate_train_data()
    generate_test_data()

if "gen-train" in args:
    generate_train_data()
if "gen-test" in args:
    generate_test_data()

if "train" in args:
    train()
    test()

if "mock-faulty" in args:
    f = args[args.index("mock-faulty") + 1]
    if os.path.exists(f):
        gen = Generator(f, is_mock = True)
        gen.generate_mock_csv(is_faulty=True)

if "mock-reliable" in args:
    f = args[args.index("mock-reliable") + 1]
    if os.path.exists(f):
        gen = Generator(f, is_mock = True)
        gen.generate_mock_csv(is_faulty=False)

if "predict" in args:
    file_to_predict = args[args.index("predict") + 1]
    if os.path.exists("data/decision-tree.pkl"):
        cart.load_tree()
        cart.predict(file_to_predict)
    else:
        program_error("Gere um modelo antes")
