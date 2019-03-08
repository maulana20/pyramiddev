from pyramid.security import Allow, Everyone

from sqlalchemy import create_engine
from sqlalchemy import ( ForeignKey )
from sqlalchemy import ( Column, Integer, String, Text )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import ( scoped_session, sessionmaker )
from sqlalchemy.orm import Session

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
	
class UserTable(Base):
	__tablename__= 'tblUser'
	user_id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey('tblGroup.group_id'))
	user_name = Column(String(50))
	password = Column(String(50))
	user_realname = Column(String(50))
	user_status = Column(String(1))
	
	def __init__(self, group_id, user_name, password, user_realname, user_status):
		self.group_id = group_id
		self.user_name = user_name
		self.password = password
		self.user_realname = user_realname
		self.user_status = user_status
	
class GroupTable(Base):
	__tablename__ = 'tblGroup'
	group_id = Column(Integer, primary_key=True)
	group_name = Column(String(50))
	group_access = Column(Text)
	
	def __init__(self, group_name, group_access):
		self.group_name = group_name
		self.group_access = group_access
	
class Root(object):
	__acl__ = [
		(Allow, 'ADMINISTRATION', 'ADMINISTRATION'),
		(Allow, 'USER', 'USER'),
		(Allow, 'GROUP', 'GROUP'),
		(Allow, 'USER_LOG', 'USER_LOG'),
		(Allow, 'OPERATIONAL', 'OPERATIONAL'),
		(Allow, 'ACCOUNTING', 'ACCOUNTING'),
		(Allow, 'COA', 'COA'),
		(Allow, 'JOURNAL', 'JOURNAL'),
		(Allow, 'GENERALLEDGER', 'GENERALLEDGER'),
		(Allow, 'TRIALBALANCE', 'TRIALBALANCE'),
		(Allow, 'BALANCESHEET', 'BALANCESHEET'),
		(Allow, 'FINANCE', 'FINANCE'),
		(Allow, 'GENERALCASHBANK', 'GENERALCASHBANK'),
		(Allow, 'INTERCASHBANK', 'INTERCASHBANK'),
		(Allow, 'POSTING', 'POSTING'),
		(Allow, 'CLOSING', 'CLOSING'),
		(Allow, 'PERIOD', 'PERIOD'),
	]
	
	def __init__(self, request):
		pass
