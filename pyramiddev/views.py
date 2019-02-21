import logging
log = logging.getLogger(__name__)

import colander
import deform.widget

from pyramid.response import Response
from pyramid.view import ( view_config, view_defaults )
from pyramid.httpexceptions import HTTPFound

pages = {
	'100': dict(uid='100', title='Page 100', body='<em>100</em>'),
	'101': dict(uid='101', title='Page 101', body='<em>101</em>'),
	'102': dict(uid='102', title='Page 102', body='<em>102</em>')
}

# @view_defaults(renderer='home.pt')
# @view_defaults(route_name='hello')
"""class PyramidDevViews:
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
	"""
	
from .models import DBSession, Page

class WikiPage(colander.MappingSchema):
	title = colander.SchemaNode(colander.String())
	body = colander.SchemaNode(colander.String(), widget=deform.widget.RichTextWidget())
	
class WikiViews(object):
	def __init__(self, request):
		self.request = request
	
	@property
	def wiki_form(self):
		schema = WikiPage()
		return deform.Form(schema, buttons=('submit',))
	
	@property
	def reqts(self):
		return self.wiki_form.get_widget_resources()
	
	@view_config(route_name='wiki_view', renderer='wiki_view.pt')
	def wiki_view(self):
		pages = DBSession.query(Page).order_by(Page.title)
		return dict(title='Wiki View', pages=pages)
	
	@view_config(route_name='wikipage_add', renderer='wikipage_addedit.pt')
	def wikipage_add(self):
		form = self.wiki_form.render()
		
		if 'submit' in self.request.params:
			controls = self.request.POST.items()
			try:
				appstruct = self.wiki_form.validate(controls)
			except deform.ValidationFailure as e:
				# Form is NOT valid
				return dict(form=e.render())
			
			# Add a new page to the database
			new_title = appstruct['title']
			new_body = appstruct['body']
			DBSession.add(Page(title=new_title, body=new_body))
			
			# Form is valid, make a new identifier and add to list
			# last_uid = int(sorted(pages.keys())[-1])
			# new_uid = str(last_uid + 1)
			# pages[new_uid] = dict(uid=new_uid, title=appstruct['title'], body=appstruct['body'])
			
			# Get the new ID and redirect
			page = DBSession.query(Page).filter_by(title=new_title).one()
			new_uid = page.uid
			
			# Now visit new page
			url = self.request.route_url('wikipage_view', uid=new_uid)
			
			return HTTPFound(url)
		
		return dict(form=form)
	
	@view_config(route_name='wikipage_view', renderer='wikipage_view.pt')
	def wikipage_view(self):
		uid = self.request.matchdict['uid']
		page = DBSession.query(Page).filter_by(uid=uid).one()
		# page = pages[uid]
		return dict(page=page)
	
	@view_config(route_name='wikipage_edit', renderer='wikipage_addedit.pt')
	def wikipage_edit(self):
		uid = self.request.matchdict['uid']
		page = DBSession.query(Page).filter_by(uid=uid).one()
		# page = pages[uid]
		
		wiki_form = self.wiki_form
		
		if 'submit' in self.request.params:
			controls = self.request.POST.items()
			try:
				appstruct = wiki_form.validate(controls)
			except deform.ValidationFailure as e:
				return dict(page=page, form=e.render())
			
			# Change the content and redirect to the view
			page['title'] = appstruct['title']
			page['body'] = appstruct['body']

			url = self.request.route_url('wikipage_view', uid=uid)
			# url = self.request.route_url('wikipage_view', uid=page['uid'])
			return HTTPFound(url)
		
		form = self.wiki_form.render(
			dict(uid=page.uid, title=page.title, body=page.body)
		)
		# form = wiki_form.render(page)
		
		return dict(page=page, form=form)
