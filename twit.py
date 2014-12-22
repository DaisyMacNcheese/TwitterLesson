#!/usr/bin/env python

''' This is a simple python application utilizing
    flask to return N tweets.
    The application communicates with the Twitter API via python-twitter
    https://github.com/bear/python-twitter
    This is largely created as a lesson in flask and APIs in general.
'''

import twitter
import yaml
import re
from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def home():
    '''This is the main route/ homepage of the application
       It sends its gathered information to the /response page
    '''
    try:
        name = request.args.get('name')
        assert name
    except:
        #name = 'Lame! What\'s your name?'
        try:
            name = request.form.get('name')
            assert name
        except:
            name = 'Lame! What\'s your name?'
    return render_template('splash.html',name=name)



@app.route("/response", methods=['GET','POST'])
def response():
    '''The /response page will display 'N' tweets from the 
       twitter handles the user has entered

       template ui (user interface) renders the results
       along with the user's name if they aren't lame
    '''
    try:
        name = request.form.get('name')
        assert name
    except:
        name = 'Lame!'

    try:
        handles = request.form.get('handles')
        assert handles
    except:
        handle = 'CBSTopNews'
        #random value selected but should never be displayed
        #since the handles form field is required

    try:
        number = request.form.get('ntweets')
        assert number
    except:
        number = 1

    auth = secauthent()

    results = []
    handles=re.split(r'[:;,\s]*',handles)

    for h in handles:
        results.append(getinfo(auth, h, number))

    anyerror=False

    for r in results:
        if not r['noerror']: anyerror=True

    return render_template('ui.html',name=name,results=results,anyerror=anyerror)

'''
########Seperating Application Logic from functions###########################
'''


def secauthent():
    '''secauthent stands for Secure Authentication.
       This function is basically a method for Authenticating
       to Twitters API.
       
       This uses YAML to read your credentials from the creds.yaml file.
       New Twitter API credentials can be obtained here.
       https://apps.twitter.com/
       
       returns the authentication needed by python-twitter
    '''
    with open('creds.yaml', 'r') as f:
        doc = yaml.load(f)

    api = twitter.Api(consumer_key       = doc['consumer_key'],
                      consumer_secret    = doc['consumer_secret'],
                      access_token_key   = doc['access_token_key'],
                      access_token_secret= doc['access_token_secret'])
    return(api)


def getinfo(authn, name, number):
    ''' Gets information about a twitter user

        :param authn: authenticated twitter api obj, output from secauthent()
        :param name: string; name of user to search for
        :param number: int; number of tweets to get

        returns a dictionary of the name and tweets
        noerror is reverse error checking on a user name lookup.
    '''

    try:
        statuses = authn.GetUserTimeline(screen_name = name,
                                         count       = number)
        tweettext = [s.text for s in statuses]
        noerror   = True
    except:
        tweettext = ['ALERT ERROR!']
        noerror   = False

    try:
        url=authn.GetUser(screen_name = name).GetProfileImageUrl()
        url=url[:-12]+'.jpeg'
    except:
        url="/static/cat_eating_bowl.jpg"

    data = {'handle': name,
            'tweets': tweettext,
           'noerror': noerror,
      'ProfileImage': url}
    return(data)


def dostuff():
    ''' legacy main function for testing 
        left here for nostalgia
        function not currently run
    '''

    auth = secauthent()

    results = []

    results.append(getinfo(auth, 'CBSTopNews', 3))
    results.append(getinfo(auth, 'CBSTopNews65e671236', 10))
    print results

    '''
    try:
        statuses=auth.GetUserTimeline(screen_name='CBSTopNew4',count=3)
        for s in statuses: print s.text
    except:
        print 'ERROR!'
    '''


if __name__ == "__main__":
    #main()
    app.debug = True
    app.run()
