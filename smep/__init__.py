__author__ = 'yi-linghwong'

import os
import sys
from flask import Flask, redirect, render_template, request, url_for, flash

from . import db
from . import get_features
from . import standardise_features
from . import run_model


app = Flask(__name__, instance_relative_config=True)

# initiate db

mysql = db.init_db(app)

# main page

@app.route('/', methods=['GET', 'POST'])
def index():

    error = None

    if request.method == 'POST':

        ##################
        # fetch form data
        ##################

        user_input = request.form
        post = user_input['user_sm_post']


        ##################
        # get media and url presence
        ##################

        has_media_checked,has_url_checked = get_features.get_media_url_presence(user_input)


        ##################
        # get LIWC feature scores
        ##################

        liwc_feature_scores = get_features.get_liwc_features(post)

        #liwc_feature_scores = [-0.59,-0.58,-0.58,-1.22,1.69,-0.58,1.7,-1.59,-1.27,1.7,0.95,-0.28,-0.11,-0.14,-0.15,-0.44,-0.41,-0.26,-0.36,-0.29,-0.33,-0.62,-0.23,3.68,1.21,-0.42,1.39,-0.38,-0.18,-0.07,-0.26,-0.23,-0.1,-0.04,-0.28,0.9,1.27,-0.12,-0.14,1.22,0.49]

        ###################
        # get hashtag presence
        ###################

        has_hashtag = get_features.check_hashtag_presence(post)


        ###################
        # construct complete features
        ###################

        feature_scores = liwc_feature_scores + [has_media_checked] + [has_hashtag] + [has_url_checked]


        ###################
        # standardise features
        ###################

        standardised_features = standardise_features.standardise_features(feature_scores)


        ###################
        # run supervised learning model
        ###################

        prediction_result,probability = run_model.predict_post(standardised_features)


        ###################
        # insert data into database
        ###################

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO userposts(text,has_media,has_url,has_hashtag,features,features_std,result,probability) "
                    "VALUES(%s,%s,%s,%s,%r,%r,%s,%s)",[post,has_media_checked,has_url_checked,has_hashtag,tuple(feature_scores),tuple(standardised_features),prediction_result,probability])
        mysql.connection.commit()
        cur.close()

        return render_template("index.html", error = error, prediction_result = prediction_result, probability = probability)

    return render_template('index.html', error = error)


if __name__ == '__main__':

    app.run(debug=True)








