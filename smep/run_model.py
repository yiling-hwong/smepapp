__author__ = 'yi-linghwong'

import os
import sys
import pickle


def predict_post(standardised_features):

    fn = os.path.join(os.path.dirname(__file__), 'models','sgd_model.sav')

    loaded_model = pickle.load(open(fn, 'rb'))

    # get test data

    X_test = [standardised_features]

    # predict

    result = loaded_model.predict(X_test)
    probability = loaded_model.predict_proba(X_test)


    if result == ['HER']:

        prediction_result = 'HIGH ENGAGEMENT'
        prob = round(probability[0][0], 3) * 100

    elif result == ['LER']:

        prediction_result = 'LOW ENGAGEMENT'
        prob = round(probability[0][1], 3) * 100

    else:

        print("error1")


    #print ()
    #print("SMEP predicts your post belongs to the " + prediction_result + ' class, with a probability of '+str(prob)+ '%')

    return prediction_result,prob


#-------------------
# test function

#predict_post([-0.61,-0.58,-0.58,-1.15,-0.6,-0.58,-0.59,0.7,-0.83,0.98,-0.56,-0.28,-0.1,-0.13,-0.15,-0.47,-0.42,-0.26,-0.37,-0.3,-0.34,0.43,-0.22,-0.22,0.66,-0.42,-0.5,-0.39,-0.17,-0.06,-0.34,-0.21,-0.1,-0.04,-0.29,0.47,1.11,-0.73,0.62])