import argparse
import validators
from modules.logger import logit,CustomError

class inputs:
    '''
        inputs class is designed to take the required and optional arguments that needed by the tool.
    '''
    def __init__(self):
        self._take_arguments()

    def _take_arguments(self):
        '''
            _take_arguments() defines the required and optinal arguments.
            For internal use and called by default by `__init__()`
        '''
        parser      = argparse.ArgumentParser()
        req         = parser.add_argument_group('Required')
        req.add_argument('-d', help='Domain name to enumrate the whois history',metavar='compnay.com',required=True)
        req.add_argument('-k', help='API key for the service, if the service is not supporting API, enter `None`',metavar='at_gixxx',required=True)
        parser.add_argument('-e',help='Enable one of supported APIs. Default value is `whoisxmlapi`',metavar='Service name',default='whoisxmlapi') 
        parser.add_argument('-v',help='Enable the verbose mode and display results in realtime, by default is False',default=False,action="store_true")

        # -- Re-ordering
        parser._action_groups.reverse() 
        
        # -- Parsing the args
        args        = parser.parse_args()
        self.args = vars(args)

        self.logit  = logit(verbose=self.args['v']) 
        self._input_validation()


    def _input_validation(self):
        '''
            _input_validation() is coded to valid the inputs and check if the input match with the criteria
            For internal use and called by default by `_take_arguments()
        '''
        try:
            if not validators.domain(self.args['d']):
                raise CustomError('c','The domain is not valid.')    
            if self.args['e'] != 'whoisxmlapi':
                raise CustomError('c','The script doesn\'t support {} API.'.format(self.args['e']))
                
        except CustomError as e:
            self.logit.add(e.criticality_level,e.message)
                
            
