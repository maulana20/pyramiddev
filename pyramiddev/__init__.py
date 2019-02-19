from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory

def hello_word(request):
	print('Incoming request')
	return Response('<body><h1>Hello Word!</h1></body>')
	
def main(global_config, **settings):
	my_session_factory = SignedCookieSessionFactory('itsaseekreet')
	config = Configurator(settings=settings, session_factory=my_session_factory)
	config.include('pyramid_chameleon')
	config.add_route('home', '/')
	config.add_route('hello', '/howdy/{first}/{last}')
	config.add_static_view(name='static', path='pyramiddev:static')
	config.scan('.views')
	return config.make_wsgi_app()
