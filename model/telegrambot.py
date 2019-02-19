import requests
import json
import time

class TelegramBot:
	def __init__(self, url, token):
		self.request = requests.session()
		self.url = url + '/bot' + token
		self.update_id = 0
	
	def send(self, method, params):
		host_url = self.url + '/' + method
		response = self.request.get(host_url, data=params);
		res_json = json.loads(response.text)
		
		return res_json['result']
		
	def last_update(self):
		last_update = []
		last_update = self.send('getUpdates', {})
		
		if len(last_update):
			self.update_id = last_update[-1]['update_id']
			last_update = self.send('getUpdates', {'offset': self.update_id})
			return last_update[0]['message']
		else:
			return last_update
		
	def refresh_update(self, update_id):
		refresh_update = []
		refresh_update = self.send('getUpdates', {'offset': update_id})
		
		if len(refresh_update):
			self.update_id = refresh_update[0]['update_id']
			return refresh_update[0]['message']
			
	def message(self, chat_id, text):
		self.send('sendMessage', {'chat_id': chat_id, 'text': text})
		
		return
		
	def run(self):
		data = []
		data = self.last_update()
		update_id = self.update_id + 1
		
		while True:
			if self.update_id > 0:
				data = self.refresh_update(update_id)
			
			if update_id == self.update_id:
				chat_id = data['chat']['id']
				text = data['text']
				self.message(chat_id, text)
				
				update_id = update_id + 1
				
				print(data['chat']['username'] + '(' + str(chat_id) + ')' + ' => ' + text)
			else:
				print('listening ..')
			time.sleep(1)

host = 'https://api.telegram.org'
token = '582054434:AAEVQ8Cdihvhw1jHv5cO-AJfF6xzLkbhugE'

telegram = TelegramBot(host, token)
telegram.run()
