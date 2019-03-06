from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from .models import ( initialize_db, get_engine_list )

from .security import groupfinder

def main(global_config, **settings):
	engine_list = get_engine_list(settings, 'sqlalchemy.')
	initialize_db(engine_list)
	my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
	config = Configurator(settings = settings, root_factory = 'pyramiddev.models.Root', session_factory = my_session_factory)
	
	# Security policies
	authn_policy = AuthTktAuthenticationPolicy( settings['pyramiddev.secret'], callback=groupfinder, hashalg='sha512' )
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	
	config.add_route('home', '/')
	config.add_route('user-list', '/user-list')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')
	config.scan()
	
	return config.make_wsgi_app()
