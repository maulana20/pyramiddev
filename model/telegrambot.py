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
		
	def last_update(self, update_id):
		update_list = []
		update_list = self.send('getUpdates', {})
		
		if len(update_list):
			if update_id > 0:
				update_list = self.send('getUpdates', {'offset': update_id})
				if len(update_list):
					self.update_id = update_list[0]['update_id']
					return update_list[0]['message']
			else:
				self.update_id = update_list[-1]['update_id']
				update_list = self.send('getUpdates', {'offset': self.update_id})
				return update_list[0]['message']
		else:
			return update_list
		
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
		data = self.last_update(0)
		update_id = self.update_id + 1
		
		while True:
			data = self.last_update(update_id)
			
			if update_id == self.update_id:
				chat_id = data['chat']['id']
				text = data['text']
				self.message(chat_id, text)
				
				update_id = self.update_id + 1
				
				fo = open('log/chat_response.txt', 'a+')
				fo.write(json.dumps(data) + "\r\n")
				fo.close
				
				print(data['chat']['username'] + '(' + str(chat_id) + ')' + ' => ' + text)
			else:
				print('listening ..')
			time.sleep(1)

host = 'https://api.telegram.org'
token = '582054434:AAEVQ8Cdihvhw1jHv5cO-AJfF6xzLkbhugE'

telegram = TelegramBot(host, token)
telegram.run()
