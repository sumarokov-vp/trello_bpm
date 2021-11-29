""" Модуль описывающий модели приложения """
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from  django.core.exceptions import ObjectDoesNotExist

from .creatio import Creatio
from .trello import TrelloConnector
from .trello_settings import BASE_URL, KEY, TOKEN
from .helpers import parse_hours


trello = TrelloConnector(
    api_url= BASE_URL,
    key= KEY,
    token= TOKEN,
)

# Create your models here.

class TrelloBoard(models.Model):
    """ Trello board model. No links """
    name = models.CharField(
        verbose_name= 'Name',
        max_length=50,
    )

    trello_id = models.CharField(
        verbose_name= 'Trello Id',
        max_length=24,
        unique=True,
    )

    url = models.CharField(
        max_length=500,
        verbose_name='Link',
        null=True,
    )

    creatio_id = models.CharField(
        verbose_name= 'Creatio Id',
        max_length= 36,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'
    
    def update_from_trello(self):
        res = trello.board(self.trello_id)
        self.url = res['shortUrl']
        self.save()

class CreatioReceipt(models.Model):
    """ Describe SLReceipt entity in Creatio """
    creatio_id = models.CharField(
        verbose_name= 'Creatio Id',
        max_length= 36,
        null=True,
    )

    number = models.CharField(
        max_length=20,
        verbose_name='Number',
        null=True,        
    )

    board = models.ForeignKey(
        TrelloBoard,
        on_delete= models.CASCADE,
        null=True,
    )

    def send_to_creatio(self, creatio_connection):
        # Создает запись Receipt в Creatio
        self.creatio_id = creatio_connection.post_receipt(self.board.creatio_id)
        return self.creatio_id
    
    def delete_from_creatio(self, creatio_connection):
        creatio_connection.delete_receipt(self.creatio_id)
    
    def count_cards_in_creatio(self, creatio_connection):
        return creatio_connection.receipt_tasks_count(self.creatio_id)

class Executor(models.Model):
    """ Describe trello card members (trello users)"""
    name = models.CharField(
        verbose_name= 'Name',
        max_length=150,
    )

    trello_id = models.CharField(
        verbose_name= 'Trello Id',
        max_length=24,
    )

    creatio_id = models.CharField(
        verbose_name= 'Creatio Id',
        max_length= 36,
        null=True,
    )

    full_name = models.CharField(
        verbose_name= 'Name',
        max_length=150,
        null=True,
    )

class TrelloList(models.Model):
    """ Класс списка на доске трелло. Ссылается на доску. На него ссылаются карточки"""
    name = models.CharField(
        verbose_name= 'Name',
        max_length=50,
    )

    trello_id = models.CharField(
        verbose_name= 'Trello Id',
        max_length=24,
        unique= True,
    )

    board_trello_id = models.CharField(
        verbose_name= 'Parent Board Id',
        max_length=24,
        null=True,
    )

    board = models.ForeignKey(
        TrelloBoard,
        on_delete= models.CASCADE,
        null=True,
    )

    cards = []

    def __str__(self):
        return f'{self.name}'
    
    def update_from_trello(self):
        response = trello.lst(self.trello_id)
        self.board_trello_id  = response['idBoard']
        self.name = response['name']
        self.save()
    
    def update_or_create_board(self, creatio_desk_id = None):
        if self.board == None:
            self.board = TrelloBoard.objects.create(trello_id= self.board_trello_id, creatio_id= creatio_desk_id)
        self.board.update_from_trello()


    def update_card_list(self):
        # возвращает список карточек списка
        response = trello.list_cards(self.trello_id)

        _cards = []
        for response_card in response:
            card, _ = TrelloCard.objects.update_or_create(
                trello_id= response_card['id'],
                defaults= {
                    'title': response_card['name'],
                    'url': response_card['shortUrl'],
                }
            )        

            for member in response_card['idMembers']:
                executor, _ = Executor.objects.get_or_create(trello_id= member)
                if executor.name is None:
                    executor.username, executor.full_name = trello.get_member_names(member)

                ExecutorInCard.objects.update_or_create(
                    card= card,
                    executor= executor,
                    defaults= {
                        'hours': 0,
                        'minutes': 0,
                    }
                )
            _cards.append(card)
        self.cards = _cards

    def send_cards_to_creatio(self, receipt: CreatioReceipt, creatio_connection: Creatio):
        for card in self.cards:
            card.receipt = receipt
            card.save()
            card.send_to_creatio(creatio_connection)

class TrelloCard(models.Model):
    """ Карточка в Трелло. В Creatio может представляться несколькими записями SLReceiptTask, в зависимости от количества исполнителей"""
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    title = models.CharField(
        verbose_name= 'Card title',
        max_length= 255,
        null=True,
    )

    trello_id = models.CharField(
        verbose_name= 'Trello Id',
        max_length=24,
        unique=True,
    )

    url = models.CharField(
        verbose_name= "Card link",
        max_length=500,
        null=True,
    )

    trello_list = models.ForeignKey(
        TrelloList,
        null=True,
        on_delete = models.CASCADE,
    )

    creatio_id = models.CharField(
        verbose_name= 'Creatio Id',
        max_length= 36,
        null=True,
    )

    executors = models.ManyToManyField(
        Executor,
        through='ExecutorInCard',
    )

    receipt = models.ForeignKey(
        CreatioReceipt,
        null=True,
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}'

    def send_to_creatio(self, creatio_connection):
        executors_records = ExecutorInCard.objects.filter(card=self)
        record: ExecutorInCard
        for record in executors_records:
            record.set_hours()
            creatio_connection.post_task(
                title= self.title,
                executor_creatio_id= record.executor.creatio_id,
                receipt_creatio_id= self.receipt.creatio_id,
                hours= record.hours,
                minutes= record.minutes,
                card_url= self.url
            )
    

class ExecutorInCard(models.Model):
    """ Дополнительное описание связи "Многие ко многим" TrelloCard - Executor, Необходима для указания часов и минут - времени исполнения"""
    card = models.ForeignKey(TrelloCard, on_delete=models.CASCADE)
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    hours = models.IntegerField(
        verbose_name= 'Hours',
    )
    minutes = models.IntegerField(
        verbose_name= 'Minutes'
    )

    def set_hours(self):
        comments = trello.get_comments(self.card.trello_id, self.executor.trello_id)
        if len(comments) > 0:
            for comment in comments:
                check, hours, minutes = parse_hours(comment['data']['text'])
                if check:
                    self.hours = hours
                    self.minutes = minutes
                    break



####################################################





@receiver(signals.post_save, sender=TrelloBoard)
def update_board(sender, instance: TrelloBoard, created, **kwargs):
    pass

@receiver(signals.post_save, sender=TrelloList)
def update_list(sender, instance: TrelloList, created, **kwargs):
    pass