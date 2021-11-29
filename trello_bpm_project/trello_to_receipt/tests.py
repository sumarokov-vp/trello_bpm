from django.test import TestCase
from unittest import skip

from .trello_settings import LIST_ID
from .models import TrelloList, CreatioReceipt, TrelloCard, ExecutorInCard
from .creatio import Creatio
from .helpers import parse_hours

TEST_LIST_ID = '5f5dba9e4abe021b0a4c619e'

TRELLO_DESK = '2F644406-C4F9-4F18-A0AC-149F38A263FC'

CREATIO_URL = 'http://bpm.simplelogic.ru'
CREATIO_LOGIN = 'Vova'
CREATIO_PASSWORD = 'd9IziUjnU9Lw'
ODATA_VERSION = "4"
# Create your tests here.
class TestCreatio(TestCase):
    def setUp(self):

        self.lst, _ = TrelloList.objects.get_or_create(trello_id= TEST_LIST_ID)
        self.lst.update_from_trello()
        self.lst.update_or_create_board(creatio_desk_id= TRELLO_DESK)
        self.lst.update_card_list()
        self.receipt = CreatioReceipt.objects.create(
            board= self.lst.board
        )

        ############

        self.creatio: Creatio

    @skip("Don't want to test")
    def test_creatio_auth(self):
        creatio = Creatio(
            creatio_host= CREATIO_URL,
            login= CREATIO_LOGIN,
            password= CREATIO_PASSWORD,
            odata_version= ODATA_VERSION,
        )
        self.assertEqual(len(creatio.headers['BPMCSRF']), 22)

    @skip("Don't want to test")
    def test_post_receipt(self):
        creatio = Creatio(
            creatio_host= CREATIO_URL,
            login= CREATIO_LOGIN,
            password= CREATIO_PASSWORD,
            odata_version= ODATA_VERSION,
        )
        self.receipt.send_to_creatio(creatio_connection= creatio)
        if len(self.receipt.creatio_id) == 36:
            self.receipt.delete_from_creatio(creatio_connection= creatio)

        self.assertEqual(len(self.receipt.creatio_id),36)

    @skip("Don't want to test")
    def test_create_task(self):
        creatio = Creatio(
            creatio_host= CREATIO_URL,
            login= CREATIO_LOGIN,
            password= CREATIO_PASSWORD,
            odata_version= ODATA_VERSION,
        )
        self.receipt.send_to_creatio(creatio_connection= creatio)
        before = self.receipt.count_cards_in_creatio(creatio_connection= creatio)
        if len(self.receipt.creatio_id) == 36:
            self.lst.send_cards_to_creatio(receipt= self.receipt, creatio_connection= creatio)
        after = self.receipt.count_cards_in_creatio(creatio_connection= creatio)
        
        self.assertNotEquals(before, after)
    
    @skip("Don't want to test")
    def test_hours_by_card(self):
        card_link = 'https://trello.com/c/VhtfvArZ'
        card = TrelloCard.objects.get(url= card_link)
        records = ExecutorInCard.objects.filter(card= card)
        total_hours = 0
        for record in records:
            record.set_hours()
            total_hours += record.hours
        
        self.assertEquals(total_hours, 2)

    #@skip("Don't want to test")
    def test_parse_hours(self):

        check, h, m = parse_hours('2:34')
        self.assertEquals(check, True)
        self.assertEquals(h, 2)
        self.assertEquals(m, 34)

        check, h, m = parse_hours('Total 2:34')
        self.assertEquals(check, True)
        self.assertEquals(h, 2)
        self.assertEquals(m, 34)

        check, h, m = parse_hours('2ч')
        self.assertEquals(check, True)
        self.assertEquals(h, 2)
        self.assertEquals(m, 0)

        check, h, m = parse_hours('40 минут всего 1:40')
        self.assertEquals(check, True)
        self.assertEquals(h, 1)
        self.assertEquals(m, 40)    

        check, h, m = parse_hours('2 часа')
        self.assertEquals(check, True)
        self.assertEquals(h, 2)
        self.assertEquals(m, 0)

        check, h, m = parse_hours('2 утки')
        self.assertEquals(check, False)

        check, h, m = parse_hours('20 минут')
        self.assertEquals(check, True)
        self.assertEquals(h, 0)
        self.assertEquals(m, 20)        

        check, h, m = parse_hours('Готово\n8h')
        self.assertEquals(check, True)
        self.assertEquals(h, 8)
        self.assertEquals(m, 0)

        check, h, m = parse_hours('Работа - 15 минут, всего 30 минут')
        self.assertEquals(check, True)
        self.assertEquals(h, 0)
        self.assertEquals(m, 30)

        check, h, m = parse_hours('1 час')
        self.assertEquals(check, True)
        self.assertEquals(h, 1)
        self.assertEquals(m, 0)

        check, h, m = parse_hours('$35 = 50 минут')
        self.assertEquals(check, True)
        self.assertEquals(h, 0)
        self.assertEquals(m, 50)

        check, h, m = parse_hours('0,5 часа')
        self.assertEquals(check, True)
        self.assertEquals(h, 0)
        self.assertEquals(m, 30)

        check, h, m = parse_hours('0.5hrs')
        self.assertEquals(check, True)
        self.assertEquals(h, 0)
        self.assertEquals(m, 30)

        check, h, m = parse_hours('Поиск причины и устранение (пустое сообщение)- 30 минут всего 2:40')
        self.assertEquals(check, True)
        self.assertEquals(h, 2)
        self.assertEquals(m, 40)

        check, h, m = parse_hours('Переделал на системные настройки - еще 30 минут всего 1 час')
        self.assertEquals(check, True)
        self.assertEquals(h, 1)
        self.assertEquals(m, 0)

        check, h, m = parse_hours('6 часов')
        self.assertEquals(check, True)
        self.assertEquals(h, 6)
        self.assertEquals(m, 0)
    
        check, h, m = parse_hours('готово\n15min')
        self.assertEquals(check, True)
        self.assertEquals(h, 0)
        self.assertEquals(m, 15)