# import matplotlib.pyplot as plt
import pandas as pd
from sklearn import model_selection, preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

h = .02  # step size in the mesh

names = ["KNN", "RBF SVM", "DT", "RF"]

classifiers = [
    KNeighborsClassifier(9),
    SVC(gamma=21, C=25),
    DecisionTreeClassifier(max_depth=7),
    RandomForestClassifier(max_depth=10, n_estimators=100)]

dataframe = pd.read_csv("cipher_reference_data.csv")
arr = dataframe.values
X = arr[:, 1:]
Y = arr[:, 0]

scaler = preprocessing.MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# results = []
# scoring = 'accuracy'
# for name, model in zip(names, classifiers):
#     kfold = model_selection.StratifiedKFold(n_splits=10, random_state=7, shuffle=True)
#     cv_results = model_selection.cross_val_score(model, X_scaled, Y, cv=kfold, scoring=scoring)
#     results.append(cv_results)
#     msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
#     print(msg)
#
# fig = plt.figure()
# fig.suptitle('Algorithm Comparison')
# ax = fig.add_subplot(111)
# plt.boxplot(results)
# ax.set_xticklabels(names)
# plt.show()


# scoring = 'accuracy'
# for neighbours in range(1, 16, 2):
#     kfold = model_selection.StratifiedKFold(n_splits=10, random_state=7)
#     cv_results = model_selection.cross_val_score(KNeighborsClassifier(neighbours), X_scaled, Y, cv=kfold,
#     scoring=scoring)
#     msg = "%d: %f (%f)" % (neighbours, cv_results.mean(), cv_results.std())
#     print(msg)


# scoring = 'accuracy'
# gammas = range(15, 25)
# for gamma in gammas:
#     kfold = model_selection.StratifiedKFold(n_splits=10, random_state=7)
#     cv_results = model_selection.cross_val_score(SVC(gamma=gamma), X_scaled, Y, cv=kfold, scoring=scoring)
#     msg = "%f: %f (%f)" % (gamma, cv_results.mean(), cv_results.std())
#     print(msg)


# scoring = 'accuracy'
# cs = range(20, 50, 5)
# for c in cs:
#     kfold = model_selection.StratifiedKFold(n_splits=10, random_state=7)
#     cv_results = model_selection.cross_val_score(SVC(gamma=21, C=c), X_scaled, Y, cv=kfold, scoring=scoring)
#     msg = "%d: %f (%f)" % (c, cv_results.mean(), cv_results.std())
#     print(msg)


# scoring = 'accuracy'
# features = range(1, len(X[0]))
# for feature in features:
#     kfold = model_selection.StratifiedKFold(n_splits=5, random_state=7)
#     cv_results = model_selection.cross_val_score(DecisionTreeClassifier(max_depth=7, max_features=feature), X_scaled,
#     Y, cv=kfold, scoring=scoring)
#     msg = "%f: %f (%f)" % (feature, cv_results.mean(), cv_results.std())
#     print(msg)


# scoring = 'accuracy'
# vars = [0]
# for var in vars:
#     kfold = model_selection.StratifiedKFold(n_splits=10, random_state=7)
#     cv_results = model_selection.cross_val_score(RandomForestClassifier(max_depth=10, n_estimators=100), X_scaled, Y,
#     cv=kfold, scoring=scoring)
#     msg = "%f: %f (%f)" % (var, cv_results.mean(), cv_results.std())
#     print(msg)


X_train, X_test, y_train, y_test = model_selection.train_test_split(X_scaled, Y, random_state=0)
clf = RandomForestClassifier(max_depth=15, n_estimators=100)
# noinspection PyUnresolvedReferences
y_pred = clf.fit(X_train, y_train).predict(X_test)
print(clf.classes_)
for row in confusion_matrix(y_test, y_pred):
    print(*row)
