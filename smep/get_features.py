__author__ = 'yi-linghwong'

import os


def get_media_url_presence(user_input):


    has_media = 'has_media' in user_input
    has_url = 'has_url' in user_input

    if has_media == 1:
        has_media_checked = 1

    else:
        has_media_checked = 0

    if has_url == 1:
        has_url_checked = 1

    else:
        has_url_checked = 0

    return has_media_checked,has_url_checked

def get_liwc_features(post):

    # get LIWC api details

    fn = os.path.join(os.path.dirname(__file__), '..','instance','liwc.csv')
    lines = open(fn,'r').readlines()

    api_dict = {}

    for line in lines[1:]:
        spline = line.rstrip('\n').split(',')
        api_dict['api_key'] = spline[0]
        api_dict['api_secret_key'] = spline[1]

    url = 'https://api-v3.receptiviti.com/v3/api/content'

    def get_api_params():
        params = {

            "content_source": 0,
            "language_content": post

        }

        return params

    def get_response_from_liwc_api():

        import requests
        import json
        import sys

        # CHECK response status (if 200, fine)


        try:
            response = requests.post(url=url, headers={'X-API-KEY': api_dict['api_key'], 'X-API-SECRET-KEY': api_dict['api_secret_key']},
                                 params=get_api_params())

            # print(response.text)

            # Consider any status other than 2xx an error
            if not response.status_code // 100 == 2:
                print (response.status_code)
                return "Error: Unexpected response {}".format(response)


        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            print (e)
            return "Error: {}".format(e)

        '''

        try:
            response.raise_for_status()

        except requests.exceptions.RequestException as e:

            print (e)
            sys.exit(1)    
        
        except requests.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            print ("Error: " + str(e))
        '''



        response_json = json.loads(response.text)

        analytic_score = response_json["liwc_scores"]["analytic"]
        clout_score = response_json["liwc_scores"]["clout"]
        authentic_score = response_json["liwc_scores"]["authentic"]
        tone_score = response_json["liwc_scores"]["tone"]

        #print (analytic_score,clout_score,authentic_score,tone_score)

        # check if summary dimension scores belong to upper or lower quartile

        if analytic_score > 98.87:
            analytic_high = 1
            analytic_low = 0

        elif analytic_score < 88.66:
            analytic_low = 1
            analytic_high = 0

        else:
            analytic_high = 0
            analytic_low = 0

        if clout_score > 76.79:
            clout_high = 1
            clout_low = 0

        elif analytic_score < 50.00:
            clout_low = 1
            clout_high = 0

        else:
            clout_high = 0
            clout_low = 0

        if authentic_score > 61.82:
            authentic_high = 1
            authentic_low = 0

        elif authentic_score < 3.8:
            authentic_low = 1
            authentic_high = 0

        else:
            authentic_high = 0
            authentic_low = 0

        if tone_score > 92.66:
            tone_high = 1
            tone_low = 0

        elif tone_score < 25.77:
            tone_low = 1
            tone_high = 0

        else:
            tone_high = 0
            tone_low = 0

        #print (analytic_high,analytic_low,clout_high,clout_low,authentic_high,authentic_low,tone_high,tone_low)

        # construct liwc features

        wps = response_json["liwc_scores"]["wps"]
        sixltr = response_json["liwc_scores"]["sixLtr"]
        posemo = response_json["liwc_scores"]["categories"]["posemo"]
        negemo = response_json["liwc_scores"]["categories"]["negemo"]
        anx = response_json["liwc_scores"]["categories"]["anx"]
        anger = response_json["liwc_scores"]["categories"]["anger"]
        sad = response_json["liwc_scores"]["categories"]["sad"]
        insight = response_json["liwc_scores"]["categories"]["insight"]
        cause = response_json["liwc_scores"]["categories"]["cause"]
        discrep = response_json["liwc_scores"]["categories"]["discrep"]
        tentat = response_json["liwc_scores"]["categories"]["tentat"]
        certain = response_json["liwc_scores"]["categories"]["certain"]
        differ = response_json["liwc_scores"]["categories"]["differ"]
        see = response_json["liwc_scores"]["categories"]["see"]
        hear = response_json["liwc_scores"]["categories"]["hear"]
        feel = response_json["liwc_scores"]["categories"]["feel"]
        affiliation = response_json["liwc_scores"]["categories"]["affiliation"]
        achieve = response_json["liwc_scores"]["categories"]["achieve"]
        power = response_json["liwc_scores"]["categories"]["power"]
        reward = response_json["liwc_scores"]["categories"]["reward"]
        risk = response_json["liwc_scores"]["categories"]["risk"]
        swear = response_json["liwc_scores"]["categories"]["swear"]
        netspeak = response_json["liwc_scores"]["categories"]["netspeak"]
        assent = response_json["liwc_scores"]["categories"]["assent"]
        nonflu = response_json["liwc_scores"]["categories"]["nonflu"]
        filler = response_json["liwc_scores"]["categories"]["filler"]
        QMark = response_json["liwc_scores"]["categories"]["QMark"]
        Exclam = response_json["liwc_scores"]["categories"]["Exclam"]


        summary_dimension_features = [analytic_high,analytic_low,clout_high,clout_low,authentic_high,authentic_low,tone_high,tone_low]
        non_summary_dimension_features = [wps,sixltr,posemo,negemo,anx,anger,sad,insight,cause,discrep,tentat,certain,differ,
                                          see,hear,feel,affiliation,achieve,power,reward,risk,swear,netspeak,assent,nonflu,filler,QMark,Exclam]

        liwc_features = summary_dimension_features + non_summary_dimension_features


        return liwc_features


    liwc_features = get_response_from_liwc_api()

    return liwc_features


def check_hashtag_presence(post):


    ################
    # replace special character at end of sentence with white space
    # so that hashtags without a space in front of them can be detected too (e.g. This is it.#space)
    ################

    post_updated = post.replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')

    ################
    # get hashtag presence
    ################

    word_list = post_updated.split()

    if any(word.startswith("#") for word in word_list):
        has_hashtag = 1

    else:
        has_hashtag = 0

    #print (has_hashtag)

    return has_hashtag


#------------------------
# test functions

#get_media_url_presence()

get_liwc_features("Today is a #happy day")

#check_hashtag_presence("Today is a #happy day")

















