import requests

class AtrisBot:
	def __init__(self, url, u_name, u_pass):
		self.request = requests.Session()
		self.url = url + '/api'
		self.u_name = u_name
		self.u_pass = u_pass
		
	def login(self):
		response = self.request.post(self.url + '/admin/login', data={'user': self.u_name, 'password': self.u_pass})
		
		fo = open('log/atris_login.txt', 'w')
		fo.write(response.text)
		fo.close()
		
	def isonlogin(self):
		response = self.request.get(self.url + '/admin/isonlogin', data={})
		
		fo = open('log/atris_isonlogin.txt', 'w')
		fo.write(response.text)
		fo.close()
		
	def logout(self):
		response = self.request.get(self.url + '/admin/logout', data={})
		
		fo = open('log/atris_logout.txt', 'w')
		fo.write(response.text)
		fo.close()
		
atris = AtrisBot('http://coba.com', 'user', 'pass')
atris.login()
atris.isonlogin()
atris.logout()
