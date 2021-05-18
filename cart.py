import graphviz
from sklearn.datasets import load_iris
from sklearn import tree

from generator import Generator
from utils.utils import parse_csv_to_data, program_error

class CART:
    def __init__(self):
        self.clf = tree.DecisionTreeClassifier()
        self.amount_of_freezers = 0
        self.amount_of_test_freezers = 0

    def generate_train_data(self, amount_of_freezers, amount_of_faulty_freezers, plot = True):
        if amount_of_freezers < 2:
            program_error("[Treino] É necessário pelo menos 2 freezers")
        if amount_of_faulty_freezers < 1:
            program_error("[Treino] É necessário pelo menos 1 freezer defeituoso")
        if amount_of_faulty_freezers > amount_of_freezers:
            program_error("[Treino] Há mais freezers no geral do que freezers defeituosos")

        self.amount_of_freezers = amount_of_freezers

        gen = Generator("data/report.csv")
        gen.generate_csv(amount_of_freezers = amount_of_freezers, amount_of_faulty_freezers = amount_of_faulty_freezers, plot = plot)

    def generate_test_data(self, amount_of_freezers, amount_of_faulty_freezers, plot = False):
        if amount_of_freezers < 2:
            program_error("[Teste] É necessário pelo menos 2 freezers")
        if amount_of_faulty_freezers < 1:
            program_error("[Teste] É necessário pelo menos 1 freezer defeituoso")
        if amount_of_faulty_freezers > amount_of_freezers:
            program_error("[Teste] Há mais freezers no geral do que freezers defeituosos")

        gen = Generator("data/report_test.csv")
        gen.generate_csv(amount_of_freezers = amount_of_freezers, amount_of_faulty_freezers = amount_of_faulty_freezers, plot = plot)

    def train(self, amount_of_freezers):
        X = []
        Y = []
        for freezer in range(amount_of_freezers):
            lx, ly = parse_csv_to_data("data/report.csv", freezer)
            for _x in lx:
                X.append(_x)
            for _y in ly:
                Y.append(_y)

        self.clf = self.clf.fit(X, Y)

    def test(self, amount_of_test_freezers):
        total_guesses = 0
        correct_guesses = 0
        for freezer in range(amount_of_test_freezers):
            X, Y = parse_csv_to_data("data/report_test.csv", freezer)
            Z = self.clf.predict(X)

            total = len(Y)
            total_guesses += total
            right = 0
            for i in range(total):
                if Y[i] == Z[i]:
                    right += 1
                    correct_guesses += 1
            print("Predição do aparelho %d está: %d%% correto!" % (freezer, (right/total)*100))

        print("Predição no geral: %d%% correto." % ((correct_guesses/total_guesses)*100))

    def generate_visualization(self):
        # r = tree.export_text(clf, feature_names=["temperature", "lastRepairYear"])#, "manufactureYear", "brand", "model"])
        # print(r)
        dot_data = tree.export_graphviz(self.clf, out_file=None,
                                            feature_names=["temperature", "lastRepairYear"],
                                            class_names=["Reliable", "Faulty"],
                                            filled=True, rounded=True,
                                            special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render(filename='data/viz')
        print("Visualização da árvore gerada em 'data/viz.pdf'")