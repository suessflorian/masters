from sklearn import tree
import graphviz

# See https://scikit-learn.org/stable/modules/tree.html#decision-trees
# For a more detail spiel...

# Typically decision trees are able to deal with both handle both numerical and
# categorical data. However, the scikit-learn implementation does not support
# categorical variables for now. Hence the need for translation from
# categorical fields to an index'd numerical representation.

# Need to translate categorical features to index's, we construct maps for
# some level of readability...
COLOURS = {"RED": 0, "BLUE": 1}
LENGTH = {"SHORT": 0, "LONG": 1}
SIZE = {"SMALL": 0, "LARGER": 1}
BRIGHTNESS = {"DULL": 0, "BRIGHT": 1}
SHAPE = {"TRIANGLE": 0, "CIRCLE": 1}
LABELS = {"FALSE": 0, "TRUE": 1}


# Every time we read results, we can reverse the maps above
def reverseMap(incomingMap):
    return dict(reversed(item) for item in incomingMap.items())


# feature_order = [COLOURS, LENGTH, SIZE, BRIGHTNESS, SHAPE]
dataset = [
    [
        COLOURS["RED"],
        LENGTH["LONG"],
        SIZE["LARGER"],
        BRIGHTNESS["BRIGHT"],
        SHAPE["TRIANGLE"],
    ],
    [
        COLOURS["RED"],
        LENGTH["LONG"],
        SIZE["SMALL"],
        BRIGHTNESS["BRIGHT"],
        SHAPE["CIRCLE"],
    ],
    [
        COLOURS["RED"],
        LENGTH["LONG"],
        SIZE["SMALL"],
        BRIGHTNESS["BRIGHT"],
        SHAPE["TRIANGLE"],
    ],
    [
        COLOURS["RED"],
        LENGTH["SHORT"],
        SIZE["LARGER"],
        BRIGHTNESS["DULL"],
        SHAPE["CIRCLE"],
    ],
    [
        COLOURS["RED"],
        LENGTH["SHORT"],
        SIZE["LARGER"],
        BRIGHTNESS["BRIGHT"],
        SHAPE["TRIANGLE"],
    ],
    [
        COLOURS["BLUE"],
        LENGTH["SHORT"],
        SIZE["LARGER"],
        BRIGHTNESS["BRIGHT"],
        SHAPE["TRIANGLE"],
    ],
]

labels = [
    LABELS["TRUE"],
    LABELS["FALSE"],
    LABELS["TRUE"],
    LABELS["FALSE"],
    LABELS["TRUE"],
    LABELS["FALSE"],
]

model = tree.DecisionTreeClassifier(criterion="entropy")
model = model.fit(dataset, labels)

graph = graphviz.Source(tree.export_graphviz(model, out_file=None))
graph.render("model")

# To perform a series of classifications using this model;

# classified = model.predict(
#     [
#         [
#             COLOURS["RED"],
#             LENGTH["SHORT"],
#             SIZE["LARGER"],
#             BRIGHTNESS["BRIGHT"],
#             SHAPE["TRIANGLE"],
#         ]
#     ]
# )

# readableClassifications = map(
#     lambda index: reverseMap(LABELS)[index], classified)
# print(list(readableClassifications))

# To print this tree in stdout we can rely on matplotlib and simply do;

# print(tree.plot_tree(model))
