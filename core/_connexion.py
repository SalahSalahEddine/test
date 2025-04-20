import requests
'''
Function Check If Valid Internet Connection ,Neccessary To Use For Other Functions To Work
#Get The Google Client And Scan The Status Code If ==> 200:So This Is Meaning Succusfull Connection
'''
def is_online():
       try:
            response = requests.get("https://www.google.com")
            if response.status_code == 200:
                #Internet Connexion Available
                return True
            else:
                #Error Connexion
                return False
       except requests.exceptions.ConnectionError:
            return False
