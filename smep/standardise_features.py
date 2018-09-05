__author__  = 'yi-linghwong'

import os
import sys
from flask import flash, render_template, redirect, url_for


def standardise_features(feature_scores):

    # get list of means and SDs

    fn = os.path.join(os.path.dirname(__file__), 'data','mean.csv')
    lines1 = open(fn,'r').readlines()

    fn = os.path.join(os.path.dirname(__file__), 'data','std.csv')
    lines2 = open(fn,'r').readlines()

    mean_values = []
    std_values = []

    for line in lines1:
        spline = line.rstrip('\n')
        mean_values.append(round(float(spline),4))

    for line in lines2:
        spline = line.rstrip('\n')
        std_values.append(round(float(spline),4))


    if len(feature_scores) == len(mean_values) == len(std_values):

        standardised_feature_list = []

        for index,s in enumerate(feature_scores):

            standardised_feature_score = (s - mean_values[index]) / std_values[index]
            standardised_feature_list.append(round(standardised_feature_score,2))

    else:

        # TO-DO ADD error handling
        error = "There has been an error. Error code: 3"

    return standardised_feature_list







#---------------
# test function

#standardise_features([0, 0, 0, 0, 0, 0, 1, 0, 2.5, 0.2, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 1, 1, 1])

