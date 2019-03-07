from .adapters import get_db_session
from .adapters import ( UserTable, GroupTable )

from phpserialize import serialize, unserialize
from io import BytesIO

class UserModel():
	def __init__(self):
		self.DBSession = get_db_session()

	def getList(self):
		res = self.DBSession.query(UserTable.user_id, GroupTable.group_name, UserTable.user_name, UserTable.user_realname, UserTable.user_status).join(GroupTable).filter(UserTable.group_id==GroupTable.group_id).filter(UserTable.user_status=='A')
		
		user_list = []
		for list in res:
			data = {}
			data['user_id'] = list.user_id
			data['user_name'] = list.user_name
			data['user_realname'] = list.user_realname
			data['group_name'] = list.group_name
			
			user_list.append(data)
		
		return user_list

	def getAcl(self, user_id):
		res = self.DBSession.query(GroupTable.group_access).join(UserTable).filter(UserTable.user_id==user_id).first()
		
		group_access = bytes(res.group_access, 'utf-8')
		group_access = unserialize(group_access)
		
		acl_list = []
		for i in group_access:
			acl_list.append(group_access[i].decode("utf-8"))

		return acl_list

	def getId(self, user_name):
		res = self.DBSession.query(UserTable.user_id).filter(UserTable.user_name==user_name).first()
		
		return res.user_id
