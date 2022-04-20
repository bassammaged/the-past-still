from modules.logger import CustomError,logit
import requests
from time import sleep
from os import path
from json import dump

def run_service(service_name,verbose,domain,api_key=None):
    if service_name == 'whoisxmlapi':
        whoisxmlapi(domain,api_key,verbose)._send_request()

class whoisxmlapi:
    '''
        whoisxmlapi class is designed to connect with `https://whois-history.whoisxmlapi.com` through valid API key.
        and filter the returned data then store it into json file or 7-chakras database.

        Arguments:
            domain: target's domain.
            api_key: api_key for the whoisxmlapi. 
            visability: holds visaiblity option
    '''
    url                     = "https://whois-history.whoisxmlapi.com/api/v1"

    def __init__(self,domain,api_key,verbose):
        self.domain     = domain
        self.api_key    = api_key
        self.logit      = logit(self.domain,verbose)

    def _send_request(self):
        '''
            _send_request() is built to send GET request to whois-history.whoisxmlapi.com with domain and api key

            Arugments:
                No arguemnts.
            
            Returns:
                JSON data.

        '''

        headers = {
            'user-agent':'7-chakras/python3'
        }

        payload = {
            'apiKey': self.api_key,
            'domainName':self.domain,
            'mode':'purchase'
        }


        conn_success = False
        count = 1
        tries = 3
        while conn_success == False and count <= tries:
            try:
                req = requests.get(self.url,headers=headers,params=payload)
                if req.status_code == 200:
                    conn_success = True
                    self.logit.add('d','The return code is 200 OK!')
                    store_data(req.json(),'json',self.domain,self.logit)
                
                elif req.status_code == 403:
                    conn_success = True
                    raise CustomError('c','Access restricted. Check the DRS credits balance or enter the correct API key.')
            except requests.exceptions.ConnectionError:
                self.logit.add('w','The script couldn\'t establish connection with the service.')
                count = count + 1
                sleep(5)
            except CustomError as e:
                self.logit.add(e.criticality_level,e.message)
            except Exception as e:
                self.logit.add('e','Unexpected Error happened. ERROR: {}'.format(e))


        if count >= tries and conn_success == False:
           self.logit.add('e','Connection has been failed {} times in a row.'.format(tries))

class store_data:
    '''
        Storing data based on the end-user preference and mode of the script.

        Arguments:
            - data: information is needed to be stored.
            - type: holds the type of file [json,csv,db]
            - domain: target's domain.
            - logit_object: takes logit object for proceed logging within the same file.

        Returns:
            No returns.

    '''
    def __init__(self,data,type,domain,logit_object):
        self.data   = data
        self.type   = type
        self.domain = domain
        self.logit  = logit_object

        if self.type == 'json':
            self._into_json()

    def _into_json(self):
        '''
            _into_json() is function built to store information in json format.
        '''
        # -- Sanitize the json data
        jsonFiltered = {}
        index = 1
        for record in self.data["records"]:
            jsonFiltered[index] = {}
            jsonFiltered[index]["registrantName"]           = record["registrantContact"]["name"]
            jsonFiltered[index]["registrantEmail"]          = record["registrantContact"]["email"]
            jsonFiltered[index]["registrantTelephone"]      = record["registrantContact"]["telephone"]
            jsonFiltered[index]["administrativeName"]       = record["administrativeContact"]["name"]
            jsonFiltered[index]["administrativeEmail"]      = record["administrativeContact"]["email"]
            jsonFiltered[index]["administrativeTelephone"]  = record["administrativeContact"]["telephone"]
            jsonFiltered[index]["technicalNamel"]           = record["technicalContact"]["name"]
            jsonFiltered[index]["technicalEmail"]           = record["technicalContact"]["email"]
            jsonFiltered[index]["technicalTelephone"]       = record["technicalContact"]["telephone"]
            index = index + 1
        try:
            with open(path.join(path.dirname(__file__),'..', self.domain + '-result.json'),'w') as result_file:
                dump(jsonFiltered,result_file)
            self.logit.add('f','Whois history had been enumrated successfully.')
        except Exception as e:
            self.logit.add('c','Unexpected error happened while storing the data into json file, ERROR: {}'.format(e))
