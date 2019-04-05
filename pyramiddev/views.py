import urllib.parse
import os
import json

import socket

from pyramid.response import Response

from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden

from pyramid.security import ( remember, forget )

from sqlalchemy.orm import joinedload

from .models import UserModel

@view_config(context=HTTPForbidden)
def error_view(exc, request):
	msg = exc.args[0] if exc.args else ""
	return Response("Forbidden: " + msg)

class PyramiddevView(object):
	def __init__(self, request):
		self.request = request
		self.logged_in = request.authenticated_userid

	@view_config(route_name='home', renderer='json')
	def home(self):
		user = UserModel()
		user_name = user.getUserName(self.logged_in) if self.logged_in else '' 
		
		return {'project': 'pyramiddev', 'username': user_name}

	@view_config(route_name='user-list', renderer='json', permission='USER')
	def user_list(self):
		user = UserModel()
		user_list = user.getList()
		
		return { 'user_list': user_list }

	@view_config(route_name='login')
	def login(self):
		request = self.request
		username = request.params['user']
		password = request.params['password']
		
		user = UserModel()
		is_userpass = user.isUserPass(username, password)
		if (is_userpass == True):
			user_id = user.getId(username)
			
			headers = remember(request, user_id)
			hostname = socket.gethostbyname(socket.gethostname()) # default localhost
			return HTTPFound(location='http://' + hostname  + ':6543/', headers=headers)
		else:
			return Response("Failed")
	
	@view_config(route_name='logout')
	def logout(self):
		request = self.request
		headers = forget(request)
		hostname = socket.gethostbyname(socket.gethostname()) # default localhost
		return HTTPFound(location='http://'+ hostname + ':6543/', headers=headers)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_rits_manual_db" script
	to initialize your database tables.  Check your virtual 
	environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
	database server referred to by the "sqlalchemy.url" setting in
	your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

