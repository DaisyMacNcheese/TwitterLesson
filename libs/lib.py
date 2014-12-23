import twitter
import yaml


def get_authenticated_api():
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
    return api


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


# def dostuff():
#     ''' legacy main function for testing 
#         left here for nostalgia
#         function not currently run
#     '''

#     auth = secauthent()

#     results = []

#     results.append(getinfo(auth, 'CBSTopNews', 3))
#     results.append(getinfo(auth, 'CBSTopNews65e671236', 10))
#     print results

#     '''
#     try:
#         statuses=auth.GetUserTimeline(screen_name='CBSTopNew4',count=3)
#         for s in statuses: print s.text
#     except:
#         print 'ERROR!'
#     '''
