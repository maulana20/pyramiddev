from .adapters import get_db_session
from .adapters import ( UserTable, GroupTable )

class UserModel():
	def __init__(self):
		self.DBSession = get_db_session()

	def getList(self):
		res = self.DBSession.query(UserTable.user_id, GroupTable.group_name, UserTable.user_name, UserTable.user_realname, UserTable.user_status).join(GroupTable).filter(UserTable.group_id==GroupTable.group_id).filter(UserTable.user_status=='A')
		
		user_list = []
		for list in res:
			print(list)
			data = {}
			data['user_id'] = list.user_id
			data['user_name'] = list.user_name
			data['user_realname'] = list.user_realname
			data['group_name'] = list.group_name
			
			user_list.append(data)
		
		return user_list
