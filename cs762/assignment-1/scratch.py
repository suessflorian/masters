import pandas as pd
from sklearn import tree

# dealing with missing data;
# https://pandas.pydata.org/docs/user_guide/missing_data.html
df = pd.read_csv('datasets/website-phishing.csv', na_values='?')
df = df.fillna(df.mean())  # as per assignment guidance

# TODO: split 70:30 training/testing
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

# link to iloc;
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html
features, labels = df.iloc[:, :-1], df.iloc[:, -1]


# decision stump
# https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
decision_stump = tree.DecisionTreeClassifier(max_depth=1, criterion="entropy")
decision_stump.fit(features, labels)

# unpruned
unpruned_tree = tree.DecisionTreeClassifier(criterion="entropy")
unpruned_tree.fit(features, labels)

# post pruned tree
# https://scikit-learn.org/stable/modules/tree.html#minimal-cost-complexity-pruning
# https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html

unpruned_tree
