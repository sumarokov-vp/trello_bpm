from django.contrib import admin
from .models import TrelloBoard, TrelloCard, TrelloList
# Register your models here.

admin.site.register(TrelloCard)
admin.site.register(TrelloBoard)
admin.site.register(TrelloList)

