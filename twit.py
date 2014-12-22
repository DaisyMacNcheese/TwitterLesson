#!/usr/bin/env python

''' This is a simple python application utilizing
    flask to return N tweets.
    The application communicates with the Twitter API via python-twitter
    https://github.com/bear/python-twitter
    This is largely created as a lesson in flask and APIs in general.
'''

import re
from flask import Flask
from flask import request
from flask import render_template
from libs.lib import get_authenticated_api
from libs.lib import getinfo


def create_app():
    ''' wrapper to creat the flask application; also confirm auth
        works before we serve up the application
    '''
    global api
    api = get_authenticated_api()
    app = Flask(__name__)
    return app

# init
app = create_app()


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

    auth = api

    results = []
    handles=re.split(r'[:;,\s]*',handles)

    for h in handles:
        results.append(getinfo(auth, h, number))

    anyerror=False

    for r in results:
        if not r['noerror']: anyerror=True

    return render_template('ui.html',name=name,results=results,anyerror=anyerror)


if __name__ == "__main__":
    app.debug = True
    app.run()
