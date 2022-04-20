from modules.arguments import inputs
from modules.whois_history import run_service


def welcome():
    msg = '''
▀▀█▀▀ ▒█░▒█ ▒█▀▀▀ 　 ▒█▀▀█ ░█▀▀█ ▒█▀▀▀█ ▀▀█▀▀ 　 ▒█▀▀▀█ ▀▀█▀▀ ▀█▀ ▒█░░░ ▒█░░░ 
░▒█░░ ▒█▀▀█ ▒█▀▀▀ 　 ▒█▄▄█ ▒█▄▄█ ░▀▀▀▄▄ ░▒█░░ 　 ░▀▀▀▄▄ ░▒█░░ ▒█░ ▒█░░░ ▒█░░░ 
░▒█░░ ▒█░▒█ ▒█▄▄▄ 　 ▒█░░░ ▒█░▒█ ▒█▄▄▄█ ░▒█░░ 　 ▒█▄▄▄█ ░▒█░░ ▄█▄ ▒█▄▄█ ▒█▄▄█
-----------------------------------------------------------------------------
   is python tool designed to enumerate the WHOIS history and extract the 
      important information that could be used in the future usage. Also, 
   `The past still` is coded to support multiple WHOIS history service APIs.
-----------------------------------------------------------------------------
                    Coded by: @bassammaged (kemet)
                            Version: 1.0
                      Supported APIs: whoisxmlapi
-----------------------------------------------------------------------------
    '''
    print(msg)

def main():
    try:
        welcome()
        obj1 = inputs()
        run_service(obj1.args['e'],obj1.args['v'],obj1.args['d'],obj1.args['k'])
    except KeyboardInterrupt:
        print('\u2718 The script has been terminated by `keyboard interrupt`')

if __name__ == '__main__':
    main()