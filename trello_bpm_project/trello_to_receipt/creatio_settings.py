from os import environ

CREATIO_URL = 'http://creatio.simplelogic.ru:5000'
CREATIO_LOGIN = environ.get('CREATIOUSER') 
CREATIO_PASSWORD = environ.get('CREATIOPASSWORD') 
ODATA_VERSION = "4core"