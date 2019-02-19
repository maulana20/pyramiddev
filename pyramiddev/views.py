import logging
log = logging.getLogger(__name__)

from pyramid.response import Response
from pyramid.view import ( view_config, view_defaults )
from pyramid.httpexceptions import HTTPFound

# @view_defaults(renderer='home.pt')
@view_defaults(route_name='hello')
class PyramidDevViews:
	def __init__(self, request):
		self.request = request
		self.view_name = 'PyramidDevViews'
	
	@property
	def counter(self):
		session = self.request.session
		if 'counter' in session:
			session['counter'] += 1
		else:
			session['counter'] = 1
		
		return session['counter']
		
	def full_name(self):
		first = self.request.matchdict['first']
		last = self.request.matchdict['last']
		return first + ' ' + last
	
	@view_config(route_name='home', renderer='home.pt')
	def home(self):
		log.debug(self.view_name)
		return { 'page_title': 'Home View' }
	
	@view_config(route_name='hello', renderer='hello.pt')
	def hello(self):
		log.debug('In Hello View')
		return { 'page_title': 'Hello View' }
	
	@view_config(request_method='POST', renderer='edit.pt')
	def edit(self):
		new_name = self.request.params['new_name']
		return { 'page_title': 'Edit View', 'new_name': new_name }
	
	@view_config(request_method='POST', request_param='form.delete', renderer='delete.pt')
	def delete(self):
		print('Deleted')
		return { 'page_title': 'Delete View' }
