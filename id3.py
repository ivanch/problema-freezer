from sklearn.datasets import load_iris
from sklearn import tree
import graphviz

from generator import Generator
from utils.utils import parse_csv_to_data

# CONSTS

# Train
AMOUNT_OF_FREEZERS = 200
AMOUNT_OF_FAULTY_FREEZERS = 100

# Test
TEST_AMOUNT_OF_FREEZERS = 500
TEST_AMOUNT_OF_FAULTY_FREEZERS = 250

# DECISION TREE (CART)

clf = tree.DecisionTreeClassifier()

# GENERATE TRAIN DATA

gen = Generator("data/report.csv")
gen.generate_csv(amount_of_freezers = AMOUNT_OF_FREEZERS, amount_of_faulty_freezers = AMOUNT_OF_FAULTY_FREEZERS, plot = True)

# TRAIN

X = []
Y = []
for freezer in range(AMOUNT_OF_FREEZERS):
    lx, ly = parse_csv_to_data("data/report.csv", freezer)
    for _x in lx:
        X.append(_x)
    for _y in ly:
        Y.append(_y)

clf = clf.fit(X, Y)

# GENERATE TEST DATA AND TEST

test_gen = Generator("data/report_test.csv")
test_gen.generate_csv(amount_of_freezers = TEST_AMOUNT_OF_FREEZERS, amount_of_faulty_freezers = TEST_AMOUNT_OF_FAULTY_FREEZERS, plot = False)

total_guesses = 0
correct_guesses = 0
for freezer in range(TEST_AMOUNT_OF_FREEZERS):
    X, Y = parse_csv_to_data("data/report_test.csv", freezer)
    Z = clf.predict(X)

    total = len(Y)
    total_guesses += total
    right = 0
    for i in range(total):
        if Y[i] == Z[i]:
            right += 1
            correct_guesses += 1
    print("Machine %d prediction is %d%% right!" % (freezer, (right/total)*100))

print("Overall prediction is %d%% right." % ((correct_guesses/total_guesses)*100))

# r = tree.export_text(clf, feature_names=["temperature", "lastRepairYear"])#, "manufactureYear", "brand", "model"])
# print(r)

dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=["temperature", "lastRepairYear"],
                                    class_names=["Reliable", "Faulty"],
                                    filled=True, rounded=True,
                                    special_characters=True)
graph = graphviz.Source(dot_data)
graph.render(filename='data/viz')