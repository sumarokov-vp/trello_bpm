""" Модуль коннектора к Трелло. Содержит методы работы с API Trello"""
import requests

from .trello_settings import BASE_URL, KEY, TOKEN

class TrelloConnector():
    """ Класс содержащий методы API Trello:"""
    def __init__(self, api_url, key, token):
        self.url = api_url
        self.key = key
        self.token = token

    def board(self, board_id):
        url = f'{BASE_URL}/boards/{board_id}?key={KEY}&token={TOKEN}'
        print('Board')
        return requests.get(url).json()
    
    def lst(self, list_id):
        url = f'{BASE_URL}/lists/{list_id}?key={KEY}&token={TOKEN}'
        response = requests.get(url).json()
        name = response['name']
        print(f'List: {name}')
        return response
    
    def list_cards(self, list_id):
        url = f'{BASE_URL}/lists/{list_id}/cards?key={KEY}&token={TOKEN}'
        print('Cards List')
        return requests.get(url).json()
    
    def get_member_names(self, member_id):
        url = f'{BASE_URL}/members/{member_id}?key={KEY}&token={TOKEN}'
        response = requests.get(url).json()
        fullname = response['fullName']
        print(f'member name: {fullname}')
        return response['username'], response['fullName']
    
    def get_comments(self, card_id, member_id):
        url = f'{BASE_URL}/cards/{card_id}/actions?key={KEY}&token={TOKEN}&filter=commentCard'
        all_comments = requests.get(url).json()
        member_comments = [d for d in all_comments if d['idMemberCreator'] == member_id]
        member_comments.sort(key=lambda item:item['date'], reverse=True)
        return member_comments
    
    def get_member_boards(self, member_id):
        url = f'{BASE_URL}/members/{member_id}/boards?key={KEY}&token={TOKEN}'
        return requests.get(url).json()        