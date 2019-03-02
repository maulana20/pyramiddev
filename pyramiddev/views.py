import urllib.parse
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden

from sqlalchemy.orm import joinedload

import os
import json

from .models import (
	User,
	Group,
	get_db_session,
	)
	
@view_config(context=HTTPForbidden)
def error_view(exc, request):
	msg = exc.args[0] if exc.args else ""
	return Response("Forbidden: " + msg)

class PyramiddevView(object):
	def __init__(self, request):
		self.request = request
		self.DBSession = get_db_session()
	
	@view_config(route_name='home', renderer='json')
	def home(self):
		return {'project': 'pyramiddev'}
	
	@view_config(route_name='user-list', renderer='json')
	def user_list(self):
		user_list = []
		
		res = self.DBSession.query(User.user_id, Group.group_name, User.user_name, User.user_realname, User.user_status).join(Group).filter(User.group_id==Group.group_id).filter(User.user_status=='A')
		for list in res:
			data = {}
			data['user_id'] = list.user_id
			data['user_name'] = list.user_name
			data['user_realname'] = list.user_realname
			data['group_name'] = list.group_name
			
			user_list.append(data)
		
		return {'user_list': user_list}
	
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

