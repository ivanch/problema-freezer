import pickle
import graphviz
from sklearn.datasets import load_iris
from sklearn import tree

from generator import Generator
from utils.utils import *

# CONST
FAULTY_THRESHOLD = 60

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
            lx, ly = parse_csv_to_data_gen("data/report.csv", freezer)
            for _x in lx:
                X.append(_x)
            for _y in ly:
                Y.append(_y)

        self.clf = self.clf.fit(X, Y)

    def analyse_result(self, result: list):
        sum = 0
        for r in result:
            if r:
                sum += 1
        return (sum/len(result))*100

    def save_tree(self):
        with open("data/decision-tree.pkl", "wb") as fid:
            pickle.dump(self.clf, fid)

    def load_tree(self):
        with open("data/decision-tree.pkl", "rb") as fid:
            self.clf = pickle.load(fid)

    def test(self, amount_of_test_freezers):
        total_guesses = amount_of_test_freezers
        correct_guesses = 0
        for freezer in range(amount_of_test_freezers):
            X, Y = parse_csv_to_data_gen("data/report_test.csv", freezer)
            Z = self.clf.predict(X)

            probability = self.analyse_result(Z)
            isFaulty = probability >= FAULTY_THRESHOLD

            print("Probabilidade de falha da máquina %d: %.2f%%." % (freezer, probability))

            if isFaulty == Y[0]:
                correct_guesses += 1

        print("Predição no geral: %d%% correto." % ((correct_guesses/total_guesses)*100))

    def predict(self, csv_path):
        X = parse_csv_to_data(csv_path)
        Z = self.clf.predict(X)
        probability = self.analyse_result(Z)

        isFaulty = probability >= FAULTY_THRESHOLD

        print("Probabilidade de falha da máquina: %.2f%%." % (probability))
        print("A máquina é considerada: %s." % ("Defeituosa" if isFaulty else "Confiável"))

    def generate_visualization(self):
        # r = tree.export_text(clf, feature_names=["temperature", "lastRepairYear"])#, "manufactureYear", "brand", "model"])
        # print(r)
        dot_data = tree.export_graphviz(self.clf, out_file=None,
                                            feature_names=["temperature", "last repair year", "manufacture year"],
                                            class_names=["Reliable", "Faulty"],
                                            filled=True, rounded=True,
                                            special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render(filename='data/viz')
        print("Visualização da árvore gerada em 'data/viz.pdf'")