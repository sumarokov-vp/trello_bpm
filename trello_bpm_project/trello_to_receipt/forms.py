from django import forms
from .models import CreatioReceipt, TrelloList

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = CreatioReceipt
        fields = ('board', 'trello_list')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trello_list'].queryset = TrelloList.objects.none()