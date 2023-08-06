# Copyright 2021 MatchTune Inc.
#
# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# MatchTune.
#
# As with any software that integrates with the MatchTune platform, your use
# of this software is subject to the MatchTune terms of services and
# Policies [https://www.matchtune.com/privacy-policy]. This copyright notice
# shall be included in all copies or substantial portions of the software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import time
import hmac
import base64
import hashlib
import requests

## Class MatchTune
##
## @package MatchTune
class MatchTune:

    ## @const string Version number of the MatchTune PHP SDK.
    VERSION                         = '1.0.0'

    ## @const string Default endpoint of MatchTune PHP SDK.
    APP_ENDPOINT_DEFAULT            = 'https://api.matchtune.com'

    ## @const string The name of the environment variable that contains the app ID.
    APP_ID_ENV_NAME                 = 'MATCHTUNE_APP_ID'

    ## @const string The name of the environment variable that contains the app secret.
    APP_SECRET_ENV_NAME             = 'MATCHTUNE_APP_SECRET'

    ## @const string The name of the environment variable that contains the app secret.
    APP_TOKEN_ENV_NAME              = 'MATCHTUNE_APP_TOKEN'

    ## @var array The configuration store.
    config                          = {}

    ## @var array The last error.
    lasterror                       = None


    ## Instantiates a new MatchTune super-class object.
    ##
    ## @param array config
    ##   You should set app_id / app_secret / app_token in the contructor or in the environment
    ##   using respectively APP_ID_ENV_NAME / APP_SECRET_ENV_NAME / APP_TOKEN_ENV_NAME
    ##
    def __init__(self, config = {}):
        self.config['app_endpoint'] = self.APP_ENDPOINT_DEFAULT

        if self.APP_ID_ENV_NAME in os.environ:
            self.config['app_id']       = os.environ[self.APP_ID_ENV_NAME]

        if self.APP_SECRET_ENV_NAME in os.environ:
            self.config['app_secret']   = os.environ[self.APP_SECRET_ENV_NAME]

        if self.APP_TOKEN_ENV_NAME in os.environ:
            self.config['app_token']    = os.environ[self.APP_TOKEN_ENV_NAME]

        for key in config:
            self.config[key]        = config[key]
        return

    ## Calls the api
    ##
    ## @param string target
    ##   The url target
    ##
    ## @param string method
    ##   HTTP Method : GET/POST/PUT/DELETE ...
    ##
    ## @param array data
    ##   (optional) Argument to send to the endpoint
    ##
    ## @return array result
    ##   returns server result or null if failed
    def callAPI(self, target, method, data = None):
        url                     = self.config['app_endpoint'] + '/' + target
        self.lasterror          = None
        response                = None

        ## Optional Authentication:
        uname                   = ''
        temp                    = os.uname()
        for key in temp:
            uname += key + ' '
        uname = uname.strip(' ')

        headers                 = {}
        headers['User-Agent']   = 'MatchTune-Python-SDK/' + self.VERSION + ' (' + uname + ')'
        headers['Content-Type']  = 'application/json'

        if self.config['app_token'] != None:
            headers['Authorization'] = 'Bearer ' + self.config['app_token']['value']

        if method == "GET":
            response            = requests.get(url = url, json = data, headers = headers)

        if method == "POST":
            response            = requests.post(url = url, json = data, headers = headers)

        data                    = response.json()
        status                  = response.status_code

        if status == 200:
          self.lasterror        = None
          return data['data']['attributes']

        if 'errors' in data:
            self.lasterror      = data['errors'].pop()
        else:
            if isinstance(data, list):
                self.lasterror  = data.pop(0)
            else:
                self.lasterror  = data

        return None


    ## Returns current JWT token for reuse
    ##
    ## @return array token
    ##   returns JWT Token
    def getCurrentToken(self):
       return self.config['app_token']


    ## Returns last server error
    ##
    ## @return string error
    ##   Returns last server error
    def getLastError(self):
       return self.lasterror


    ## Retreive api version
    ##
    ## @return string version
    ##   Returns API Version
    def apiVersion(self):
        result = self.callAPI('version', 'GET')
        return result['version']

    ## Login to API using apikey
    ##
    ## @param string client_id
    ##   Identification for the client ex device UUID, account identification, email etc ...
    ##
    ## @param boolean tos
    ##   Acceptation of the terms of services as listed https://www.matchtune.com/privacy-policy
    ##
    ## @return boolean
    ##   True if successfull, False otherwise
    def apiLogin(self, client_id, tos):
        app_id                   = self.config['app_id']
        app_secret               = self.config['app_secret']
        unixtime                 = int(time.time())
        payload                  = str(unixtime) + client_id + app_id
        dig                      = hmac.new(bytes(app_secret, 'utf-8'), msg=bytes(payload, 'utf-8'), digestmod=hashlib.sha256).digest()
        signature                = base64.b64encode(dig).decode()

        attributes               = {}
        attributes['UNIXTIME']   = unixtime
        attributes['UUID']       = client_id
        attributes['APPId']      = app_id
        attributes['tos']        = tos
        attributes['signature']  = signature

        data                     = {'data' : {'type' : 'tokens', 'attributes' : attributes}}

        result = self.callAPI('tokens', 'POST', data)
        if result != None:
            self.config['app_token'] = result
            return True

        return False


    ## Login to API using login and password
    ##
    ## @param string email
    ##   If no API key is available, API can be use with standard email/password method
    ##
    ## @param string password
    ##   Password of the user
    ##
    ## @return boolean
    ## True if successfull, False otherwise
    def standardLogin(self, email, password):
        data = {'data' : {'type' : 'tokens', 'attributes' : {'email' : email, 'password' : password}}}

        result = self.callAPI('tokens', 'POST', data)
        if result != None:
            self.config['app_token'] = result
            return True

        return False

    ## Retreive all available genre
    ##
    ## @return array of genres
    def genres(self):
        result = self.callAPI('classifiers', 'GET')
        if result != None:
            return result["genres"]

        return None


    ## Assemble a search query
    ##
    ## @param string genre
    ##   Genre from the list of genre (possible to send an array of genre)
    ##
    ## @param string title
    ##   Title of a known matrix (possible to send an array of title)
    ##
    ## @param array tags
    ##   Query to search using meaningfull tag words
    ##
    ## @return array formated dictionnary
    def makeQuery(self, genre = None, subgenre = None, title = None, tags = None):
        query = {}
        if genre != None:
            query['genres']            = genre

        if title != None:
            query['title']             = title

        if tags != None:
            query['tags']              = tags

        return query


    ## Assemble a feature query
    ##
    ## @param int timecode
    ##   Set a climax at this time code in milliseconds
    ##
    ## @param boolean withRiser
    ##   Enhence the climax using a riser sound effect before the climax
    ##
    ## @param boolean withDrop
    ##   Enhence the climax using a drop sound effect after the climax
    ##
    ##
    ## @return array formated dictionnary
    def makeClimaxFeature(self, timecode, withRiser = True, withDrop = True):
        feature = {}
        feature['cursor']            = timecode
        feature['cutAfterPoint']     = True
        feature['followingPartType'] = 'climax'
        feature['isFinal']           = False
        feature['addonsTypes']       = []
        if withRiser:
            feature['addonsTypes'].append('riser')

        if withDrop:
            feature['addonsTypes'].append('drop')


        return feature


    ## Filter ai-generated musics
    ##
    ## @param array card
    ##   id card as received from generation
    ##
    ## @return array filtered output
    def _filterIDCard(self, card):
        if isinstance(card, list):
            card = card[0]
        output = {}
        output['license']              = card['license']
        output['finalHash']            = card['finalHash']
        output['metadata']             = card['metadata']
        output['metadata']['duration'] = card['totalDuration']
        output['urls']                 = card['urls']

        return output


    ## Retreive ai-generated musics
    ##
    ## @param array query
    ##   Use the result from makeQuery()
    ##
    ## @return array idcard
    def generate(self, query = {}):
        data = {'data' : {'type' : 'search', 'attributes' : query}}

        result = self.callAPI('search', 'POST', data)
        if result != None:
            return self._filterIDCard(result)

        return False


    ## Customize ai-generated musics
    ##
    ## @param array query
    ##   Use the result from makeQuery()
    ##
    ## @param array features
    ##   Use a list of results from makeClimaxFeature()
    ##
    ## @return array
    ##   Returns a new id card
    def customize(self, duration, query = {}, features = {}):
        attributes               = query
        attributes['duration']   = duration
        attributes['syncPoints'] = features

        data = {'data' : {'type' : 'search', 'attributes' : attributes}}
        result = self.callAPI('search', 'POST', data)
        if result != None:
            return self._filterIDCard(result)

        return False


    ## Customize ai-generated musics
    ##
    ## @param string finalHash
    ##   Use the finalHash of an existing id card
    ##
    ## @param int duration
    ##   Choose a new duration to change lenght
    ##
    ## @param array features
    ##   Use a list of results from makeClimaxFeature()
    ##
    ## @return array
    ##   Returns a new id card
    def modify(self, finalHash, duration, features = {}):
        attributes                     = {}
        attributes['finalHash']        = finalHash
        attributes['duration']         = duration
        attributes['syncPoints']       = features

        data = {'data' : {'type' : 'search', 'attributes' : attributes}}

        result = self.callAPI('search', 'POST', data)
        if result != None:
            return self._filterIDCard(result)

        return False


    ## License one or many ai-generated musics
    ## see https://www.matchtune.com/license-information for more details
    ## applyCharges automatically purchase the track, api user can automatically set it to true
    ## users that logs in with a regular account (not an api key) should first retreive a quote using applyCharges = false
    ## api users can only purchase premium licenses
    ##
    ## @param string finalHash
    ##   Use the finalHash of an existing id card
    ##
    ## @param string license
    ##   License type standard or premium, api user may only select premium license
    ##
    ## @param boolean applyCharges
    ##   API users may directly set applyCharges to True
    ##   Standard users should request a quote using applyCharges = False then confirm the buy using applyCharges = True
    ##
    ## @return array
    ##   Price or credit applied (usefull when regular login, api user are charged after use based on volume)
    def license(self, finalHash, license = 'premium', applyCharges = True):
        attributes                     = {}
        attributes['finalHash']        = None
        attributes['license']          = license
        attributes['applyCharges']     = applyCharges

        if isinstance(finalHash, list):
            attributes['finalHash']    = finalHash
        else:
            attributes['finalHash']    = [finalHash]

        data = {'data' : {'type' : 'purchase', 'attributes' : attributes}}

        result = self.callAPI('musics/purchase', 'POST', data)
        if result != None:
            return result

        return False


    ## get an url for a known music
    ##
    ## @param string finalHash
    ##   Use the finalHash of an existing id card
    ##
    ## @param string quality
    ##   Available qualities are protected, low, high, lossless
    ##   If the music is not licensed only the protected version is available.
    ##   Note : protected means low quality with watermark
    ##
    ## @return string
    ##   Returns a fresh temporary URL to use for preview or download
    def getMusicURL(self, finalHash, quality):
        data = None

        result = self.callAPI('musics/' + finalHash + '/download?quality=' + quality + '&forwarding=false', 'GET', data)
        if result != None:
            return result

        return False
