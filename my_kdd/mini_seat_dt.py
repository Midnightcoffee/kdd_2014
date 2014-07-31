"""
File: mini_seat_dt.py
Author: Drew Verlee
Email:  Drew.verlee@gmail.com
Github: Midnightcoffee
Description: Building a mini decision tree classifier for to decide to take 
a flight delay for a given amount of reimbursement
"""


import os
import numpy as np
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.metrics import roc_auc_score



# Columns describe attributes such as "Ticket price"
#column 0 = business (0) or pleasure (1) bp
#column 1 = reimbursement (r)


# ----- narrative -----------
# first lets plot some sample data with these rules
# people flying business never say yes
# people flying pleasure say yes if over 50


# Build data (X)

     #bp,r  , outcome {yes: 1, no: 0}
X = [[0, 90], # 0 
     [0, 80], # 0
     [0, 70], # 0
     [0, 60], # 0
     [0, 50], # 0
     [0, 40], # 0
     [0, 30], # 0
     [0, 20], # 0
     [0, 10], # 0
     [0, 0],  # 0 Now pleasure
     [1, 90], # 1
     [1, 80], # 1
     [1, 70], # 1
     [1, 60], # 1
     [1, 50], # 0
     [1, 40], # 0
     [1, 30], # 0
     [1, 20], # 0
     [1, 10], # 0
     [1, 0],  # 0
     ] 

# build our Y, by copying the outcome that fits are narrative above
bussines = [0] * 10
pleasure_over_50 = [1] * 4
pleasure_under_50 = [0] * 6
pleasure = pleasure_over_50 + pleasure_under_50

Y = bussines + pleasure

# Now we build our tree
classifier = tree.DecisionTreeClassifier()

# Find the fit
classifier = classifier.fit(X,Y)

# --------------- Creating a pdf of tree ------------

# Some extra code just to turn it into a dot file 
with open("mini_seat_dt.dot", "w") as a_file:
    a_file = tree.export_graphviz(classifier, out_file=a_file)

# from there, to turn it into a pdf, you have to run
#os.unlink('test.dot')
# and then dot -Tpdf file_name.dot -o file_name.pdf

#How to read the graph.
# Take a look at our root node, x[0] refers to business vs pleasure (bp)
# gini refers to the importance of a decision in this case bp
# The root address if the reimbursement is over 50 i.e x[1] <= 55
# and this correctly splits 12 to No and 8 to Yes
# then we split on the second level on if its business or pleasure




# first we create some new data to test against
# we expect the outcome ..
new_data = [
        [0, 15], # 0
        [0, 95], # 0
        [1, 15], # 0
        [1, 95], # 1
        ]

predicted = classifier.predict(new_data)

#predicted = [0, 0, 0, 1], as expected


# -------------- AUC of ROC --------------------------
# now we find the AUC of ROC


# to find the AUC of the ROC we first assign some true labels/outcomes
actual_outcome =  [0, 0, 0, 1]
y_true = np.array(actual_outcome)

# and compare that to our predicted
y_scores = np.array(predicted)
auc_score = roc_auc_score(y_true, y_scores)
print auc_score

#auc_score = 1, as it should in this case






