from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory

from sqlalchemy import engine_from_config

from .models import DBSession, Base

# def hello_word(request):
#	print('Incoming request')
#	return Response('<body><h1>Hello Word!</h1></body>')
	
def main(global_config, **settings):
	engine = engine_from_config(settings, 'sqlalchemy.')
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine
	
	# my_session_factory = SignedCookieSessionFactory('itsaseekreet')
	# config = Configurator(settings=settings, session_factory=my_session_factory)
	config = Configurator(settings=settings, root_factory='pyramiddev.models.Root')
	config.include('pyramid_chameleon')
	# config.add_route('home', '/')
	# config.add_route('hello', '/howdy/{first}/{last}')
	# config.add_static_view(name='static', path='pyramiddev:static')
	
	# deform
	config.add_route('wiki_view', '/')
	config.add_route('wikipage_add', '/add')
	config.add_route('wikipage_view', '/{uid}')
	config.add_route('wikipage_edit', '/{uid}/edit')
	config.add_static_view('deform_static', 'deform:static/')

	config.scan('.views')
	return config.make_wsgi_app()
