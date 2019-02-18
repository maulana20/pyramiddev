import requests
import json

class TelegramBot:
	def __init__(self, url, token):
		self.url = url + '/bot' + token
	
	def send(self, method, params):
		host_url = self.url + '/' + method
		response = requests.get(host_url, data=params);
		res_json = json.loads(response.text)
		
		return res_json['result']
	
telegrambot = TelegramBot('https://api.telegram.org', '582054434:AAEVQ8Cdihvhw1jHv5cO-AJfF6xzLkbhugE')
params = {}
telegram_update = telegrambot.send('getUpdates', params)

update_id = telegram_update[-1]['update_id']
params = {}
if update_id:
	params['offset'] = update_id
telegram_update = telegrambot.send('getUpdates', params)

chat_id = telegram_update[-1]['message']['chat']['id']
params = {'chat_id': chat_id, 'text': 'hai'}
telegrambot.send('sendMessage', params)

print('running')
