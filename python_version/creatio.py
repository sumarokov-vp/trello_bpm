import json
import requests



# CREATIO_URL = 'http://crm.dragonmoney.vn'
# ODATA_VERSION = 3

SERVICE_LINKS = {
    '3': '/0/ServiceModel/EntityDataService.svc',
    '4': '/0/odata'
}

HEADERS_TEMPLATE = {
    'Content-Type':'application/json; charset=utf-8',
    'ForceUseSession':'true',
    'Accept':'application/json; charset=utf-8',
    'BPMCSRF': '',
}


RECEIPT_OBJECT_NAME = 'SLReceipt'
TASK_OBJECT_NAME = 'SLReceiptTask'
DESK_OBJECT_NAME = 'SLTrelloDesks'
LEAD_OBJECT_NAME = 'Lead'

class Creatio():
    def __init__(self, creatio_host, login, password, odata_version):
        self.creatio_url = creatio_host
        self.odata_version: str = odata_version
        self.odata_service_link = self.creatio_url + SERVICE_LINKS[self.odata_version]
        self.headers = HEADERS_TEMPLATE
        self.forms_auth(login, password)
        self.headers['BPMCSRF'] = self.cookies['BPMCSRF']

    def forms_auth(self, login, password):
        """ Аутентификация ODATA """
        url = f'{self.creatio_url}/ServiceModel/AuthService.svc/Login'
        dict_data = {
            "UserName": login,
            'UserPassword': password,
        }
        json_data = json.dumps(dict_data)
        response = requests.post(url=url, headers=self.headers, data= json_data)
        self.cookies = response.cookies
        return

    def create_object(self, object_name, data):
        """ CREATE запрос в Creatio """
        if self.odata_version =='3':
            url = self.odata_service_link + f"/{object_name}Collection"
        else:
            url = self.odata_service_link + f"/{object_name}"
        json_data = json.dumps(data)
        response = requests.post(
            url=url,
            headers=self.headers,
            data= json_data,
            cookies= self.cookies,
        )

        if self.odata_version =='3':
            object_id = json.loads(response.content)['d']['Id']
        else:
            object_id = json.loads(response.content)['Id']

        return object_id


    def delete_object(self, object_name: str, object_id: str):
        """ DELETE запрос к Creatio """
        if self.odata_version == '3':
            url = self.odata_service_link + f"/{object_name}Collection(guid'{object_id}')"
        else:
            url = self.odata_service_link + f"/{object_name}({object_id})"

        response = requests.delete(
            url=url,
            headers=self.headers,
            cookies= self.cookies,
        )
        return response.status_code

    def post_receipt(self, board_creatio_id):
        """ Создать экземпляр SLReceipt  в Creatio """
        dict_data = {
            'SLTrelloDeskId': board_creatio_id,
        }
        return self.create_object(RECEIPT_OBJECT_NAME, dict_data)
    
    def post_lead(self, register_method, country, lead_stage, activity_result, full_name, mobile_phone, amount, term):
        """ Create Lead instance in Creatio """
        dict_data = {
            'Contact': full_name,
            'MobilePhone': mobile_phone,
            'RegisterMethodId': register_method,
            'CountryId': country,
            'QualifyStatusId': lead_stage,
            'UsrActivityResultId': activity_result,
            'UsrMoneyAmount': amount,
            'UsrTerm':str(term),
            #'UsrPhoneNumberValidated':cu.verification_passed
        }
        return self.create_object(RECEIPT_OBJECT_NAME, dict_data)

    def delete_receipt(self, receipt_creatio_id):
        status_code: int = self.delete_object(RECEIPT_OBJECT_NAME, receipt_creatio_id)
        return status_code

    def post_task(self, title, executor_creatio_id, receipt_creatio_id, hours, minutes, card_url):
        """ Создать экземпляр SLTrelloTask """
        dict_data = {
            'SLName': title,
            'SLExecutorId': executor_creatio_id,
            'SLHours': hours,
            'SLMinutes': minutes,
            'SLCardLink': card_url,
            'SLReceiptId': receipt_creatio_id,
        }
        return self.create_object(TASK_OBJECT_NAME, dict_data)

    def receipt_tasks_count(self, receipt_creatio_id):
        """ Количество тасков в рецепте в Creatio """
        if self.odata_version == '3':
            url = (
                f"{self.odata_service_link}/{TASK_OBJECT_NAME}Collection" +
                f"?$filter={RECEIPT_OBJECT_NAME}/Id eq guid'{receipt_creatio_id}'"
            )
            response = requests.get(
                url= url,
                headers=self.headers,
                cookies= self.cookies,
            )
            array = json.loads(response.content)['d']['results']
        else:
            url = (
                f"{self.odata_service_link}/{TASK_OBJECT_NAME}" +
                f"?$filter={RECEIPT_OBJECT_NAME}/Id eq {receipt_creatio_id}"
            )
            response = requests.get(
                url= url,
                headers=self.headers,
                cookies= self.cookies,
            )
            array = json.loads(response.content)['value']
        return len(array)