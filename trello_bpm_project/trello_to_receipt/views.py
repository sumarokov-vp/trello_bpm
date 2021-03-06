from django.shortcuts import render

from .models import CreatioReceipt, TrelloList, TrelloBoard
from .forms import ReceiptForm
from .creatio import Creatio
from .creatio_settings import CREATIO_URL, CREATIO_LOGIN, CREATIO_PASSWORD, ODATA_VERSION


# Create your views here.
def index(request):
    context = {'cards': [], 'cnt': 0}
    if request.method == 'POST':
        creatio = Creatio(
            creatio_host= CREATIO_URL,
            login= CREATIO_LOGIN,
            password= CREATIO_PASSWORD,
            odata_version= ODATA_VERSION,
        )
        lst, _ = TrelloList.objects.get_or_create(trello_id= 'LIST_ID')
        lst.update_from_trello()
        lst.update_or_create_board()
        receipt = CreatioReceipt.objects.create(board= lst.board)
        receipt.save()
        receipt.send_to_creatio(creatio)
        if len(receipt.creatio_id) == 36:
            lst.update_card_list()

            lst.send_cards_to_creatio(receipt, creatio)

            counter = len(lst.cards)
            context['cnt']= counter
            context['cards'] = lst.cards
    return render(request, 'trello/index.html', context)

def create_receipt(request):
    lists = TrelloList.objects.all()
    if request.method == 'POST':
        list_trello_id = request.POST['dd_trello_id']

        creatio = Creatio(
            creatio_host= CREATIO_URL,
            login= CREATIO_LOGIN,
            password= CREATIO_PASSWORD,
            odata_version= ODATA_VERSION,
        )
        lst, _ = TrelloList.objects.get_or_create(trello_id= list_trello_id)
        lst.update_from_trello()
        lst.update_or_create_board()
        receipt = CreatioReceipt.objects.create(board= lst.board)
        receipt.save()
        receipt.send_to_creatio(creatio)
        if len(receipt.creatio_id) == 36:
            lst.update_card_list()
            lst.send_cards_to_creatio(receipt, creatio)

    return render(request, 'trello/cascading_lists.html', {'lists': lists})