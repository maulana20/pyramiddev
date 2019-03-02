from pyramid.security import Allow, Everyone

from sqlalchemy import (
	Column,
	Index,
	Integer,
	String,
	Text,
	ForeignKey,
	create_engine,
	Numeric,
	DateTime,
	Float,
	)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
	relationship,
	Session,
	)

from zope.sqlalchemy import ZopeTransactionExtension

import logging
log = logging.getLogger(__name__)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
__DBSession = {}
Base = declarative_base()

HR = '---'

def initialize_db(engine_list):
	url_template = engine_list['sqlalchemy.url']
	engine_db_list = {engine: engine_list[engine] for engine in engine_list if engine.endswith('.db')}
	for engine in engine_db_list:
		site = engine.split('.')[1]
		url = url_template.replace('{DB}', engine_db_list[engine])
		
		__DBSession[site] = {}
		__DBSession[site]['engine'] = create_engine(url, pool_size=60)
	
def get_engine_list(settings, startswith):
	return {key: settings[key] for key in settings if key.startswith(startswith)}
	
def get_db_session():
	session = None
	
	engine = __DBSession['localhost']['engine']
	session = Session(bind=engine)
	
	return session
	
class User(Base):
	__tablename__= 'tblUser'
	user_id = Column(Integer, primary_key=True)
	user_name = Column(String(50))
	user_realname = Column(String(50))
	user_status = Column(String(1))
	
	def __init__(self, user_name, user_realname, user_status):
		self.user_name = user_name
		self.user_realname = user_realname
		self.user_status = user_status
	
class Root(object):
	__acl__ = [(Allow, Everyone, 'view')]
	
	def __init__(self, request):
		pass
