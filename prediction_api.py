

import urllib2, urllib, json, csv, time


CLIENT_ID = '[your id]'
CLIENT_SECRET = '[your secret]'
REDIRECT_URI = '[redirect uri]'
KEY = '[your key]'

PREDICTION_ID = 'stanford-datafest-v3'
CLOUD_STORAGE = 'stanford-datafest-2012/training_data.csv'

# INPUT FILE ***SHOULD NOT*** CONTAIN HEADER ROWS
INPUT_FILE = 'test_data.csv'
OUTPUT_FILE = 'prediction_results.csv'
INPUT_FILE_COLUMN_NAMES = [
    'fips',
    'Per Capita Income',
    'Percent College Degree',
    'Percent White',
    'Percent Black',
    'Percent Asian',
    'Percent Hispanic',
    'Percent Female',
    'Percent Voting Age Citizens',
    'Population',
    'Median Age'
]

def authorize():
  ''' Authorizes the user using OAuth 2.0. '''
  print 'Visit the URL below in a browser to authorize'
  print '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code' % \
    ('https://accounts.google.com/o/oauth2/auth',
    CLIENT_ID,
    REDIRECT_URI,
    'https://www.googleapis.com/auth/prediction')
  
  auth_code = raw_input('Enter authorization code (parameter of URL): ')
  
  data = urllib.urlencode({
    'code': auth_code,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
  })
  request = urllib2.Request(
      url='https://accounts.google.com/o/oauth2/token',
      data=data)
  request_open = urllib2.urlopen(request)
  
  response = request_open.read()
  
  tokens = json.loads(response)
  access_token = tokens['access_token']
  return access_token

def get_model(token):
  serv_req = urllib2.Request(
      'https://www.googleapis.com/prediction/v1.4/trainedmodels/%s?%s' % \
      (PREDICTION_ID, urllib.urlencode({'key': KEY, 'access_token': token})))
  
  serv_resp = urllib2.urlopen(serv_req)
  content = serv_resp.read()
  jsoncontent = json.loads(content)
  result = jsoncontent['trainingStatus']
  return result 

def train(token):
  ''' Train a model '''
  data = """{
     "id": "%s",
     "storageDataLocation": "%s"
    }""" % (PREDICTION_ID, CLOUD_STORAGE)
  headers = {"Content-type": "application/json"}

  serv_req = urllib2.Request(
      'https://www.googleapis.com/prediction/v1.4/trainedmodels?%s' % \
      urllib.urlencode({'key': KEY, 'access_token': token}),
      headers=headers, data=data)
  serv_resp = urllib2.urlopen(serv_req)
  print serv_resp.read()

def predict(token):
  ''' Predicts the result '''
  headers = {'Content-type': 'application/json'}

  inputfile = csv.reader(open(INPUT_FILE, 'r'))
  outputfile = open(OUTPUT_FILE, 'w')
  outputfile.write('%dem,' + ','.join(INPUT_FILE_COLUMN_NAMES) + '\n')
  linecount = 0
  for line in inputfile:
    linecount+=1
    if linecount >= 2710:
      predict_data = """{
        "input":{
          "csvInstance":[%s]
        }
      }""" % ','.join(line[1:])
    
      serv_req = urllib2.Request(
          'https://www.googleapis.com/prediction/v1.4/trainedmodels/%s/predict?%s' % \
          (PREDICTION_ID, urllib.urlencode({'key': KEY, 'access_token': token})),
          headers=headers, data=predict_data)
  
      try:
        serv_resp = urllib2.urlopen(serv_req)
        content = serv_resp.read()
        jsoncontent = json.loads(content)
        val = jsoncontent['outputValue']
        outputfile.write('%f' % val + ',' + ','.join(line) + '\n')
        print line
        print content
      except urllib2.HTTPError as e:
        print e.read()
      time.sleep(1)


if __name__ == "__main__":
  token = authorize()
  train(token)
  time.sleep(1)
  status = get_model(token)
  while status == 'RUNNING':
    time.sleep(1)
    status = get_model(token)
  if status = 'DONE':
    predict(token)
  else:
    print status
  
  