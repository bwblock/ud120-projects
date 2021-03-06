#! /usr/bin/env python

"""
K-Means clustering
"""

import pickle
import numpy
import matplotlib.pyplot as plt
import sys
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

def Draw(pred, features, poi, mark_poi=False, name="image.png", f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """

    ### plot each cluster with a different color--add more colors for
    ### drawing more than five clusters

    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])

    ### if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()


### load in the dict of dicts containing all the data on each person in the dataset
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
### there's an outlier--remove it!

data_dict.pop("TOTAL", 0)


### the input features we want to use
### can be any key in the person-level dictionary (salary, director_fees, etc.)
feature_1 = "salary"
feature_2 = "exercised_stock_options"
feature_3 = "total_payments"

poi  = "poi"
features_list = [poi, feature_1, feature_2, feature_3]
data = featureFormat(data_dict, features_list)
poi, finance_features = targetFeatureSplit( data )

salary_data = [float(x[1]) for x in data if float(x[0]) != 0]
options_data = [float(x[2]) for x in data if float(x[1]) != 0]

#salary_data.append(200000.)
#options_data.append(1000000.)

# ------------------- Feature scaling --------------- #

scaler = MinMaxScaler()

options_data = scaler.fit_transform(options_data)
salary_data = scaler.fit_transform(salary_data)

#print salary_data
#print salary_data[-1]
#print options_data[-1]


#print min(stock_data), "min exercised stock options"
#print max(stock_data), "max exercised stock options"

#print min(salary_data), "min salary"
#print max(salary_data), "max salary"




### in the "clustering with 3 features" part of the mini-project,
### you'll want to change this line to
### for f1, f2, f3 in finance_features:
### (as it's currently written, the line below assumes 2 features)

for f1, f2, f3 in finance_features:
#for f1, f2 in finance_features:
    plt.scatter( f1, f2 )
plt.show()

###  ----------------------  Clustering using KMeans ---------------------- ###

pred = KMeans(n_clusters=2, init='random', max_iter=200).fit_predict(data)

### rename the "name" parameter when you change the number of features
### so that the figure gets saved to a different file
try:
    Draw(pred, finance_features, poi, mark_poi=False, name="multi_clusters.pdf", f1_name=feature_1, f2_name=feature_2)
except NameError:
    print "no predictions object named pred found, no clusters to plot"
