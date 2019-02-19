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
		
	def last_update(self):
		last_update = []
		last_update = self.send('getUpdates', {})
		
		if len(last_update):
			last_update = self.send('getUpdates', {'offset': last_update[-1]['update_id']})
		
		return last_update[0]['message']
		
	def message(self, chat_id, text):
		self.send('sendMessage', {'chat_id': chat_id, 'text': text})
		
		return
		
	def run(self):
		last_update = []
		last_update = self.last_update()
		
		if len(last_update):
			chat_id = last_update['chat']['id']
			text = last_update['text']
			self.message(chat_id, text)
		
		return 'listening ..'

host = 'https://api.telegram.org'
token = '582054434:AAEVQ8Cdihvhw1jHv5cO-AJfF6xzLkbhugE'

telegram = TelegramBot(host, token)
last_update = telegram.run()
print(last_update)
