from sklearn.datasets import load_iris
from sklearn import tree
import graphviz

from generator import Generator
from utils import parse_csv_to_data

AMOUNT_OF_FREEZERS = 50
AMOUNT_OF_FAULTY_FREEZERS = 25

# gen = Generator()
# gen.generate_csv(amount_of_freezers = AMOUNT_OF_FREEZERS, amount_of_faulty_freezers = AMOUNT_OF_FAULTY_FREEZERS, plot = True)

clf = tree.DecisionTreeClassifier(criterion="entropy")

X = []
Y = []
for freezer in range(AMOUNT_OF_FREEZERS):
    lx, ly = parse_csv_to_data(freezer)
    for _x in lx:
        X.append(_x)
    for _y in ly:
        Y.append(_y)

clf = clf.fit(X, Y)

total_guesses = 0
correct_guesses = 0
for freezer in range(AMOUNT_OF_FREEZERS):
    X, Y = parse_csv_to_data(freezer)
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

# dot_data = tree.export_graphviz(clf, out_file=None)
# graph = graphviz.Source(dot_data)
# graph.render("freezers")

dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=["temperature", "lastRepairYear"],
                                    class_names=["Reliable", "Faulty"],
                                    filled=True, rounded=True,
                                    special_characters=True)
# print(dot_data)
graph = graphviz.Source(dot_data)
graph.render(filename='viz')