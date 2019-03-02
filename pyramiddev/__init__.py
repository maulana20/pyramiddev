from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config

from .models import DBSession, Base, initialize_db, get_engine_list

def main(global_config, **settings):
	engine_list = get_engine_list(settings, 'sqlalchemy.')
	initialize_db(engine_list)
	my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
	config = Configurator(settings = settings, root_factory = 'pyramiddev.models.Root', session_factory = my_session_factory)
	
	config.add_route('home', '/')
	config.add_route('user-list', '/user-list')
	config.scan()
	
	return config.make_wsgi_app()
