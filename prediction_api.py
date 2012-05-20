

import urllib2, urllib, json, csv


client_id = "[your client id]"
client_secret = "[your secret]"
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
key = "[your key]"


print 'Visit the URL below in a browser to authorize'
print '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code' % \
  ('https://accounts.google.com/o/oauth2/auth',
  client_id,
  redirect_uri,
  'https://www.googleapis.com/auth/prediction')

#4. Google redirects the user back to your web application and
#   returns an authorization code
auth_code = raw_input('Enter authorization code (parameter of URL): ')

#5. Your application requests an access token and refresh token from Google
data = urllib.urlencode({
  'code': auth_code,
  'client_id': client_id,
  'client_secret': client_secret,
  'redirect_uri': redirect_uri,
  'grant_type': 'authorization_code'
})
request = urllib2.Request(
  url='https://accounts.google.com/o/oauth2/token',
  data=data)
request_open = urllib2.urlopen(request)

#6. Google returns access token, refresh token, and expiration of
#   access token
response = request_open.read()
request_open.close()

tokens = json.loads(response)
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

prediction_id = "stanford-datafest-2012-v2"
data = """{
   "id": "%s",
   "storageDataLocation": "stanford-datafest-2012/ACS_Elections_v2.csv"
  }""" % (prediction_id)
headers = {"Content-type": "application/json"}

inputfile = csv.reader(open('real_test_data.csv', 'r'))
outputfile = open('prediction_output.csv', 'w')
for line in inputfile:
  predict_data = """{
    "input":{
      "csvInstance":[%s]
    }
  }""" % ','.join(line)

  # PREDICT NEW DATA
  serv_req = urllib2.Request("https://www.googleapis.com/prediction/v1.4/trainedmodels/%s/predict?%s" % \
                             (prediction_id, urllib.urlencode({"key": key, "access_token": access_token})),
                             headers=headers, data=predict_data)
  
  try:
    serv_resp = urllib2.urlopen(serv_req)
    content = serv_resp.read()
    jsoncontent = json.loads(content)
    val = jsoncontent['outputValue']
    outputfile.write('%f' % val + ',' + ','.join(line) + '\n')
    print content
  except urllib2.HTTPError as e:
    print e.read()



'''

# GET MODEL
serv_req = urllib2.Request("https://www.googleapis.com/prediction/v1.4/trainedmodels/%s?%s" % \
                           (prediction_id, urllib.urlencode({"key": key, "access_token": access_token})))


serv_resp = urllib2.urlopen(serv_req)
print serv_resp.read()

# TRAIN DATA
serv_req = urllib2.Request("https://www.googleapis.com/prediction/v1.4/trainedmodels?%s" % urllib.urlencode({"key": key, "access_token": access_token}),
                           headers=headers, data=data)




predict_data = """{
  "input":{
    "csvInstance":["wow fusion is awesome stories fusiontablestalks", 1, 0, 0]
  }
}"""


# GET INFO
serv_req = urllib2.Request("https://www.googleapis.com/prediction/v1.4/trainedmodels/%s?%s" % \
                           (prediction_id, urllib.urlencode({"key": key, "access_token": access_token})))

'''

